#! /usr/bin/python3
# -*- coding: utf-8 -*-

from interface import *
from player import Player
import random
import math
import time

t = time.time()
player = Player(name = "Toto", isBot = True)


def setOfGames(player, isTraining, nbOfGames, display) :
    # isTraining = True for a training session, False for a test session
    text = "TRAINING ; " if isTraining else "PLAYING ; "

    player.setBehaviour(isTraining)

    with Game(display = display, returnFeatures = 1) as game :
        currentStep = 0
        for i in range(nbOfGames) :
            if isTraining :
                player.updateConstants(explorationRate= 0.6 *( 1 - currentStep / 1000))

            done = False
            observation, reward, done = game.game_step(0)
            player.buffer = observation
            while not done:
                action = player.play()
                observation, reward, done = game.game_step(action)
                player.addStateSequence(action, reward, observation)
                player.training(currentStep)
                player.updateStats(reward)
                currentStep += 1

            print(text + "Game : {} ; Step : {}".format(i+1, currentStep))
            player.displayStats()
            player.resetStats()
            game.reset()


def testing(display = 0) :
    network2restore = 10000
    nbOfGames = 10
    player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = network2restore)
    setOfGames(player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def training() :
    nbOfGames = 10000
    setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = 0)
    player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
    print("\n{}\n".format(time.time() - t))

training()
# testing(1)
