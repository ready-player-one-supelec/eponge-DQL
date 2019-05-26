#! /usr/bin/python3
# -*- coding: utf-8 -*-

from interface import *
from player import Player
import random
import math
import time

t = time.time()
player = Player(name = "Toto")


def setOfGames(player, isTraining, nbOfGames, display) :
    # isTraining = True for a training session, False for a test session
    text = "TRAINING ; " if isTraining else "PLAYING ; "

    player.setBehaviour(isTraining)

    with Game(display = display, returnFeatures = 0, difficulty = 0) as game :
        currentStep = 0

        for i in range(nbOfGames) :
            if isTraining :
                tmp = 0.2- 0.18 * i / (nbOfGames / 2)
                if tmp > 0.02 :
                    player.updateConstants(explorationRate= tmp)
                else :
                    player.updateConstants(explorationRate= 0.02)

            done = False
            observations = []
            for _ in range(2) :
                observation, reward, done = game.game_step(0)
                observations.append(observation)

            player.buffer = np.transpose(observations, [1, 2, 0])
            tmp = currentStep
            while not done :
                player.training(currentStep)
                action = player.play()
                observation, reward, done = game.game_step(action)
                observations.pop(0)
                observations.append(observation)

                if player.score >= 200 :
                    game.reset()
                    done = True

                player.addStateSequence(action, reward, observations)
                player.updateStats(reward)
                currentStep += 1

            print(text + "Game : {} ; Steps survived : {}".format(i+1, currentStep - tmp))
            player.displayStats()
            player.resetStats()
            if player.score >= 200 :
                player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = i)
                break


def testing(display = 0) :
    network2restore = 4000
    nbOfGames = 10
    player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = network2restore)
    setOfGames(player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def training() :
    nbOfGames = 5000
    setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = 0)
    # player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
    print("\n{}\n".format(time.time() - t))

training()
# testing(1)
