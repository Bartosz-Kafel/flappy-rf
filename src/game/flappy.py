from game.bird import Bird
from game.pillar import Pillar
import pygame, os

pygame.init()

# Variables
running = True

# Const Variables
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
GAME_SCALE = 2
GAME_SPEED = 1.5
FONT = pygame.font.SysFont("Comicsansms", 32)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setting up the display
screen = pygame.display.set_mode((SCREEN_WIDTH * GAME_SCALE, SCREEN_HEIGHT * GAME_SCALE))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Importing images
def import_image(image_name, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
    image = pygame.image.load(os.path.join(BASE_DIR, "assets", "sprites", image_name)).convert_alpha()
    scaled_image = pygame.transform.scale(image, (width * GAME_SCALE, height * GAME_SCALE))

    return scaled_image

background = import_image("background.png")
floor = import_image("floor.png", 64, 32)
restart = import_image("restart.png", 192, 42)
pillar_image = import_image("pillar.png", 32, 128)

# Importing the bird

# Functions
def create_background(screen, background, x):
    screen.blit(background, (x, 0))
    screen.blit(background, (x + background.get_width(), 0))
    x -= 0.25
    if x <= -background.get_width():
        x = 0

    return x

def create_floor(screen, floor, x):
    screen.blit(floor, (x, SCREEN_HEIGHT * GAME_SCALE - floor.get_height()))
    for i in range(1, 6):
        screen.blit(floor, (x + i * floor.get_width(), SCREEN_HEIGHT * GAME_SCALE - floor.get_height()))

    x -= GAME_SPEED
    if x <= -floor.get_width():
        x = 0

    return x

# Load Game
def load_game():
    global background_x, floor_x, pillar_cooldown, bird, pillars, score
    background_x = 0
    floor_x = 0
    pillar_cooldown = 0
    score = 0

    bird_image = import_image("bird.png", 16 * 1.5, 12 * 1.5)
    bird = Bird(SCREEN_WIDTH * GAME_SCALE // 4, SCREEN_HEIGHT * GAME_SCALE // 2, bird_image)

    pillars = []

# Game initialization
load_game()
def update_display(screen):
    global background_x, score, pillar_cooldown, pillar_image, pillars, bird, floor_x

    if bird.die == False:
        background_x = create_background(screen, background, background_x)

        bird.update()
        bird.check_floor_collision((SCREEN_HEIGHT - 32) * GAME_SCALE)
        bird.draw(screen)

        pillar_cooldown += GAME_SPEED

        if pillar_cooldown >= 250:
            pillar_image = import_image("pillar.png", 32, 128)
            pillars.append(Pillar(SCREEN_WIDTH * GAME_SCALE, pillar_image))
            pillar_cooldown = 0

        for pillar in pillars:
            pillar.update(GAME_SPEED)
            pillar.draw(screen)

            if bird.check_collision(pillar):
                bird.die = True

            if bird.y < 0 and bird.x == pillar.x:
                bird.die = True
            elif bird.y >= pillar.passage_y - pillar.gap_size // 2 and bird.y <= pillar.passage_y + pillar.gap_size // 2 and bird.x == pillar.x:
                score += 1

            if pillar.check_erase():
                pillars.remove(pillar)

        floor_x = create_floor(screen, floor, floor_x)

    else:
        screen.blit(restart, ((SCREEN_WIDTH * GAME_SCALE - restart.get_width()) // 2, (SCREEN_HEIGHT * GAME_SCALE - restart.get_height()) // 2))
        if pygame.mouse.get_pressed()[0]:
            load_game()

    text_surface = FONT.render(str(score), True, (255, 255, 255))
    screen.blit(text_surface, ((SCREEN_WIDTH * GAME_SCALE) // 2 - text_surface.get_width() // 2, 10))

    pygame.display.update()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    update_display(screen)
    clock.tick(60)
