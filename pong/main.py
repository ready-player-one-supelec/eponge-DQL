#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random
import math

player = Player(name = "Toto", isBot = True)

def test(player, display = False) :
    with Game(display = display) as game :
        for i in range(1) :
            player.exploiting = True
            done = False
            game.setLimit(200)
            currentStep = 0
            while not (done or currentStep > game.limit) :
                currentObservation = game.observation
                action = player.play(currentObservation)
                observation, reward, done = game.step(action)
                currentStep += 1
                print("Playing ; Step : {} ; Action = {}".format(currentStep, action))
                # input()
            game.reset()

def train(player) :
    nbOfTrainings = 1000
    player.updateConstants(discountFactor = 0.99)
    learningRateTable = [0.05, 0.01, 0.005, 0.001]
    index = int(nbOfTrainings // len(learningRateTable))
    with Game(display = False) as game :
        for i in range(nbOfTrainings) :
            if i % index == 0 :
                player.updateConstants(learningRate = learningRateTable[i // index])
            player.updateConstants(explorationRate=(0.55 + 0.45 * math.cos(math.pi * i / nbOfTrainings)))
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

train(player)
