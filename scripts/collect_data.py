from game.bird import Bird
from game.pillar import Pillar
from game.flappy import FlappyEnv
from utils.data_collector import dataColl
import pygame, os, csv

pygame.init()
flappyenv = FlappyEnv()
data = dataColl()
clock = pygame.time.Clock()
action = 0
running = True
best_score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                action = 1

    if flappyenv.score > best_score:
        best_score = flappyenv.score

    flappyenv.step(action, best_score, True)
    data.run(flappyenv)
    action = 0
    clock.tick(60)