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

    with Game(display = display, returnFeatures = 1) as game :
        currentStep = 0
        i = 0
        observation, reward, done = game.game_step(0)
        player.buffer = observation

        while currentStep < 3000000 and i < nbOfGames:
            if isTraining :
                player.updateConstants(explorationRate= 0.1 - 0.0999 * currentStep / 3000000) #max(0,0.6 - 0.55 * currentStep / 10000))

            action = player.play()
            observation, reward, done = game.game_step(action)

            if player.score >= 50 :
                game.reset()
                done = True

            player.addStateSequence(action, reward, observation)
            player.updateStats(reward)
            currentStep += 1

            if done :
                i += 1
                print(text + "Game : {} ; Step : {} ; Reward : {}".format(i, currentStep, reward))
                player.displayStats()
                player.resetStats()
                if i % 100 == 0 or player.score >= 50 :
                    player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = i)
                observation, reward, done = game.game_step(0)
                player.buffer = observation

            player.training(currentStep)


def testing(display = 0) :
    network2restore = 500
    nbOfGames = 10
    player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = network2restore)
    setOfGames(player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def training() :
    nbOfGames = 10000
    setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = 0)
    # player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
    print("\n{}\n".format(time.time() - t))

training()
# testing(1)
