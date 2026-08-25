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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data.save_to_csv()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                action = 1

    flappyenv.step(action)
    data.run(flappyenv)
    action = 0
    clock.tick(60)