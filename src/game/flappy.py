from game.bird import Bird
from game.pillar import Pillar
from ml import DecisionTree
from utils import dataColl
import pygame, os, time
import pandas as pd

pygame.init()

class FlappyEnv: # Making a class effectivly allows to reuse the game across multiple instances, which is really useful for obtaining data for an ai agent
    def __init__(self):
        # Constant Variables
        self.SCREEN_WIDTH = 256
        self.SCREEN_HEIGHT = 256
        self.GAME_SCALE = 2
        self.FONT1 = pygame.font.SysFont("Comicsansms", 32)
        self.FONT2 = pygame.font.SysFont("Comicsansms", 16)
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH * self.GAME_SCALE, self.SCREEN_HEIGHT * self.GAME_SCALE))
        
        self.game_speed = 1.5
        self.background_x = 0
        self.floor_x = 0
        self.pillar_cooldown = 0
        self.score = 0
        self.sent = False

        self.dt = DecisionTree()
        self.dc = dataColl()

        self.dt.load_tree()

        self.load_images()

        self.bird_image = self.import_image("bird.png", 16 * 1.5, 12 * 1.5)
        self.bird = Bird(self.SCREEN_WIDTH * self.GAME_SCALE // 4, self.SCREEN_HEIGHT * self.GAME_SCALE // 2, self.bird_image)

        self.bird_image_ai = self.import_image("bird.png", 16 * 1.5, 12 * 1.5)
        self.bird_image_ai.set_alpha(128)
        self.bird_ai = Bird(self.SCREEN_WIDTH * self.GAME_SCALE // 4, self.SCREEN_HEIGHT * self.GAME_SCALE // 2, self.bird_image_ai)


        self.pillars = []

    def reset(self):
        self.__init__()

    def import_image(self, image_name, width, height):
        image = pygame.image.load(os.path.join(self.BASE_DIR, "assets", "sprites", image_name)).convert_alpha()
        scaled_image = pygame.transform.scale(image, (width * self.GAME_SCALE, height * self.GAME_SCALE))
        return scaled_image

    def load_images(self):
            self.background = self.import_image("background.png", self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            self.floor = self.import_image("floor.png", 64, 32)
            self.restart = self.import_image("restart.png", 192 // 2, 42 // 2)
            self.pillar_image = self.import_image("pillar.png", 32, 128)
            self.pillar_body_image = self.import_image("pillar_body.png", 32, 128)

    def create_background(self, screen, background, x):
        screen.blit(background, (x, 0))
        screen.blit(background, (x + background.get_width(), 0))
        x -= 0.25
        if x <= -background.get_width():
            x = 0
        
        return x

    def create_floor(self, screen, floor, x):
        screen.blit(floor, (x, self.SCREEN_HEIGHT * self.GAME_SCALE - floor.get_height()))
        for i in range(1, 6):
            screen.blit(floor, (x + i * floor.get_width(), self.SCREEN_HEIGHT * self.GAME_SCALE - floor.get_height()))

        x -= self.game_speed
        if x <= -floor.get_width():
            x = 0

        return x

    def get_data(self, bird):

        data = self.dc.get_state(self, bird)
        sample = pd.Series(
               [
                   int(data["pipe_dist_x"] // 16),
                   int(data["pipe_dist_y"] // 20),
                   int(data["bird_y"] // 5),
                   int(data["bird_vel"] // 1),
               ],
               index=["dist_x", "dist_y", "axis_y", "vel_y"],
           )
        return sample

    ### Seperating Section ###

    def step(self, action, best_score, ai=False, with_ai=False):
        if not self.bird.die:
            self.background_x = self.create_background(self.screen, self.background, self.background_x)

            if with_ai == True and not self.bird_ai.die:
                sample = self.get_data(self.bird_ai)
                action_ai = self.dt.predict(sample)
            
                self.bird_ai.action = action_ai
            
                self.bird_ai.update()
                self.bird_ai.check_floor_collision((self.SCREEN_HEIGHT - 32) * self.GAME_SCALE)
                self.bird_ai.draw(self.screen)

            self.bird.action = action

            self.bird.update()
            self.bird.check_floor_collision((self.SCREEN_HEIGHT - 32) * self.GAME_SCALE)
            self.bird.draw(self.screen)

            self.floor_x = self.create_floor(self.screen, self.floor, self.floor_x)

            self.pillar_cooldown += self.game_speed

            # Fix 1: Read time_between_pillars from class directly instead of uninstantiated self.pillar
            if self.pillar_cooldown >= 250:
                self.pillars.append(Pillar(self.SCREEN_WIDTH * self.GAME_SCALE, self.pillar_image, self.pillar_body_image))
                self.pillar_cooldown = 0

            for pillar in self.pillars[:]:
                pillar.update(self.game_speed)
                pillar.draw(self.screen)

                if self.bird.check_collision(pillar):
                    self.bird.die = True

                if with_ai == True:
                    if self.bird_ai.check_collision(pillar):
                        self.bird_ai.die = True

                if self.bird.y < 0 and self.bird.x == pillar.x:
                    self.bird.die = True
                elif self.bird.y >= pillar.passage_y - pillar.gap_size // 2 and self.bird.y <= pillar.passage_y + pillar.gap_size // 2 and self.bird.x >= pillar.x:
                    if not pillar.pillar_passed:
                        self.score += 1
                        pillar.pillar_passed = True

                if pillar.check_erase():
                    self.pillars.remove(pillar)

            self.sent = False

        else:
            if with_ai:
                if self.bird.die and not self.bird_ai.die:
                    text_surface = self.FONT1.render("AI Wins", True, (220, 20, 60))
                    self.screen.blit(text_surface, ((self.SCREEN_WIDTH * self.GAME_SCALE) // 2 - text_surface.get_width() // 2, 200))
                    if self.sent == False:
                        print("AI Won")
                        self.sent = True
                else:
                    text_surface = self.FONT1.render("Player Wins", True, (220, 20, 60))
                    self.screen.blit(text_surface, ((self.SCREEN_WIDTH * self.GAME_SCALE) // 2 - text_surface.get_width() // 2, 200))
                    if self.sent == False:
                        print("Player Won")
                        self.sent = True
            else: 
                self.screen.blit(self.restart, ((self.SCREEN_WIDTH * self.GAME_SCALE - self.restart.get_width()) // 2, (self.SCREEN_HEIGHT * self.GAME_SCALE - self.restart.get_height()) // 2))

            if pygame.mouse.get_pressed()[0]:
                self.reset()

            if ai == True:
                self.reset()

        text_surface = self.FONT1.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(text_surface, ((self.SCREEN_WIDTH * self.GAME_SCALE) // 2 - text_surface.get_width() // 2, 10))

        text_surface_best = self.FONT2.render(str(best_score), True, (255, 255, 255))
        self.screen.blit(text_surface_best, ((self.SCREEN_WIDTH * self.GAME_SCALE) // 2 - text_surface_best.get_width() // 2, 45))

        pygame.display.update()