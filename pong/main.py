#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random

player = Player(name = "Toto", isBot = True)
player.updateConstants(explorationRate=0)

with Game(display = True) as game :
    i = 0
    done = False
    while not (done or i > game.limit) :
        currentObservation = game.observation
        action = player.play(currentObservation)
        observation, reward, done = game.step(action)
        player.addStateSequence(currentObservation, action, reward, observation)
        i += 1
        print(done, i)
        # game.wait()
