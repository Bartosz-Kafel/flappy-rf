from game.bird import Bird
from game.pillar import Pillar
from game.flappy import FlappyEnv
import pygame, os

pygame.init()
flappyenv = FlappyEnv()
clock = pygame.time.Clock()
action = 0  
best_score = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                action = 1

    if flappyenv.score > best_score:
        best_score = flappyenv.score

    flappyenv.step(action, best_score)
    action = 0
    clock.tick(60)