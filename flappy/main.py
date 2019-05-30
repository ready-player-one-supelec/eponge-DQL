#! /usr/bin/python3 -u
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

    with Game(display = display, returnFeatures = 1, difficulty = 2) as game :
        currentStep = 0

        for i in range(nbOfGames) :
            if isTraining :
                tmp = 0.5 * 0.99**i
                if tmp > 0.01 :
                    player.updateConstants(explorationRate= tmp)
                else :
                    player.updateConstants(explorationRate= 0.01)

            done = False
            # observations = []
            # for _ in range(2) :
            #     observation, reward, done = game.game_step(0)
            #     observations.append(observation)
            #
            # player.buffer = np.transpose(observations, [1, 2, 0])
            observation, reward, done = game.game_step(0)
            player.buffer = observation

            tmp = currentStep
            while not done :
                player.training(currentStep)
                action = player.play()
                observation, reward, done = game.game_step(action)
                # observations.pop(0)
                # observations.append(observation)

                if player.score >= 200 :
                    game.reset()
                    done = True

                player.addStateSequence(action, reward, observation)
                player.updateStats(reward)
                currentStep += 1

            print(text + "Game : {} ; Steps survived : {}".format(i+1, currentStep - tmp))
            player.displayStats()
            if player.score >= 10 :
                player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = i)
            #    break
            player.resetStats()

def testing(display = 0) :
    network2restore = 2988
    nbOfGames = 10
    player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = network2restore)
    setOfGames(player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def training() :
    nbOfGames = 5000
    setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = 0)
    player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
    print("\n{}\n".format(time.time() - t))

# training()
testing(1)
