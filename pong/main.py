#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random

player = Player(name = "Toto", isBot = False)

with Game(display = True) as game :
    currentObservation = game.observation
    i = 0
    done = False
    while not done :
        action = player.play()
        observation, reward, done = game.step(action)
        player.addStateSequence(currentObservation, action, reward, observation)
        i += 1
        print(done, i)
        # game.wait()
