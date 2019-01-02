#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random
import math

player = Player(name = "Toto", isBot = True)

def setOfGames(player, isTraining, nbOfGames, display) :
    # isTraining = True for a training session, False for a test session
    text = "TRAINING ; " if isTraining else "PLAYING ; "

    player.updateConstants(discountFactor = 0.99)
    learningRateTable = [0.05, 0.01, 0.005, 0.001]
    index = int(nbOfGames // len(learningRateTable))
    player.setBehaviour(isTraining)

    with Game(display = display) as game :
        for i in range(nbOfGames) :
            if isTraining :
                if i % index == 0 :
                    player.updateConstants(learningRate = learningRateTable[i // index])
                player.updateConstants(explorationRate=0*(0.55 + 0.45 * math.cos(math.pi * i / nbOfGames)))

            currentStep = 0
            done = False
            observations = [game.observation]
            for _ in range(3) :
                observation, reward, done = game.step(player.play(None))
                observations.append(observation)
                currentStep += 1
            while not (done or currentStep > game.limit) :
                action = player.play(observations)
                observation, reward, done = game.step(action)
                previousState = observations[:]
                observations.pop(0)
                observations.append(observation)
                player.addStateSequence(previousState, action, reward, observations)
                player.updateStats(reward)
                currentStep += 1
                print(text + "Game : {} ; Step : {} ; Action : {}".format(i+1, currentStep, action))
                # game.wait()
            player.displayStats()
            player.resetStats()
            player.addStateSequence2trainingData()
            player.training()
            game.reset()

# player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfTrainings)
# player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfTrainings)

setOfGames(player=player, isTraining=True, nbOfGames=1000, display=False)
