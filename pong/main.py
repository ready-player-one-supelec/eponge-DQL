#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random

nbOfTrainings = 10
player = Player(name = "Toto", isBot = True)

with Game(display = False) as game :
    for i in range(nbOfTrainings) :
        game.setLimit(min(2000, 100 * i))
        player.updateConstants(explorationRate=max(0.999 ** i, 0.1))
        currentStep = 0
        done = False
        while not (done or currentStep > game.limit) :
            currentObservation = game.observation
            action = player.play(currentObservation)
            observation, reward, done = game.step(action)
            player.addStateSequence(currentObservation, action, reward, observation)
            player.updateStats(reward)
            currentStep += 1
            print("LEARNING ", i, currentStep)
            # game.wait()
        player.displayStats()
        player.resetStats()
        player.addStateSequence2trainingData()
        player.training()
        game.reset()

player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfTrainings)
# player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfTrainings)

with Game(display = True) as game :
    for i in range(10) :
        player.exploiting = True
        done = False
        currentStep = 0
        while not (done or currentStep > game.limit) :
            currentObservation = game.observation
            action = player.play(currentObservation)
            observation, reward, done = game.step(action)
            currentStep += 1
            print("PLAYING ", i, currentStep)
        game.reset()
