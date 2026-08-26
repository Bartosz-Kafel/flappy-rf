from game.bird import Bird
from game.pillar import Pillar
from game.flappy import FlappyEnv
from utils import dataColl
from ml import DecisionTree
import pygame, os
import pandas as pd

pygame.init()
flappyenv = FlappyEnv()
clock = pygame.time.Clock()
action = 0
best_score = 0
dt = DecisionTree()
dc = dataColl()
dt.load_tree()
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

    flappyenv.step(action, best_score, False, True)
    action = 0
    clock.tick(60)