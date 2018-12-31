#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
import random

actions = [0,4,5]

with Game(True) as game :
    i = 0
    done = False
    while not done :
        action = random.choice(actions)
        observation, reward, done, info = game.step(action)
        i += 1
        print(done, i)
        # game.wait()
