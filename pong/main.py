#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random

player = Player(name = "Toto", isBot = True)
player.updateConstants(explorationRate=0)

with Game(display = False) as game :
    for i in range(2) :
        currentStep = 0
        done = False
        while not (done or currentStep > game.limit) :
            currentObservation = game.observation
            action = player.play(currentObservation)
            observation, reward, done = game.step(action)
            player.addStateSequence(currentObservation, action, reward, observation)
            currentStep += 1
            print(done, currentStep)
            # game.wait()
        player.addStateSequence2trainingData()
        player.training()
        game.reset()
