from game.bird import Bird
from game.pillar import Pillar
from game.flappy import FlappyEnv
import pygame, os

pygame.init()
flappyenv = FlappyEnv()
clock = pygame.time.Clock()
action = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                action = 1

    flappyenv.step(action)
    action = 0
    clock.tick(60)