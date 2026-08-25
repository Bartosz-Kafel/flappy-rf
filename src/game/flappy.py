from game.bird import Bird
import pygame, os

pygame.init()

# Variables
running = True
background_x = 0

# Const Variables
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
GAME_SCALE = 2
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

# Importing the bird
bird = Bird(SCREEN_WIDTH * GAME_SCALE // 4, SCREEN_HEIGHT * GAME_SCALE // 2, 16 * GAME_SCALE, 16 * GAME_SCALE)

# Functions
def create_background(screen, background, x):
    screen.blit(background, (x, 0))
    screen.blit(background, (x + background.get_width(), 0))
    x -= 0.5
    if x <= -background.get_width():
        x = 0

    return x

def update_display(screen):
    screen.fill((0, 0, 0))

    global background_x
    background_x = create_background(screen, background, background_x)
    bird.update()
    bird.draw(screen)

    pygame.display.update()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_display(screen)
    clock.tick(60)
