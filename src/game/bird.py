import pygame, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def import_image(image_name, width, height):
    image = pygame.image.load(os.path.join(BASE_DIR, "assets", "sprites", image_name)).convert_alpha()
    scaled_image = pygame.transform.scale(image, (width * 2, height * 2))

    return scaled_image


class Bird():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.die = False
        self.gravity = 0.4
        self.jump_strength = -8
        self.image = import_image("bird.png", width, height)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def jump(self):
        self.velocity_y = self.jump_strength

    def update(self):
        if not self.die:
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            self.rect.center = (self.x, self.y)

    def check_floor_collision(self, floor_y):
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.die = True
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)