from game.bird import Bird
from game.pillar import Pillar
from game.flappy import FlappyEnv
from ml.classification_tree import DecisionTree
from utils.data_collector import dataColl
import pygame, os
import pandas as pd

pygame.init()
flappyenv = FlappyEnv()
clock = pygame.time.Clock()
dt = DecisionTree()
dc = dataColl()
dt.load_tree()
action = 0  
running = True
best_score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # dc.run(flappyenv)

    data = dc.get_state(flappyenv, flappyenv.bird)
    sample = pd.Series( 
        [
            int(data["pipe_dist_x"] // 16),
            int(data["pipe_dist_y"] // 20),
            int(data["bird_y"] // 5),
            int(data["bird_vel"] // 1),
        ],
        index=["dist_x", "dist_y", "axis_y", "vel_y"],
    )

    action = dt.predict(sample)

    if flappyenv.score > best_score:
        best_score = flappyenv.score

    flappyenv.step(action, best_score, True, False)
    action = 0
    clock.tick(3000)