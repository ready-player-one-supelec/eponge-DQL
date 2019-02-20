#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
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

    with Game(display = display) as game :
        currentStep = 0
        for i in range(nbOfGames) :
            if isTraining :
                tmp = 1 - 0.98 * i / 100000
                if tmp > 0.02 :
                    player.updateConstants(explorationRate= tmp)
                else :
                    player.updateConstants(explorationRate= 0.02)

            done = False
            observation = game.observation
            nouvelleObservation, reward, done = game.random_step()
            differenceObservation = nouvelleObservation - observation
            observation = nouvelleObservation
            currentStep += 1
            player.buffer = differenceObservation

            while not done:
                action = player.play()
                nouvelleObservation, reward, done = game.step(action)
                differenceObservation = nouvelleObservation - observation
                observation = nouvelleObservation
                player.addStateSequence(action, reward, differenceObservation)
                player.training(currentStep)
                player.updateStats(reward)
                currentStep += 1

            print(text + "Game : {} ; Step : {}".format(i+1, currentStep))
            player.displayStats()
            player.resetStats()
            game.reset()

def testing(display = False) :
    network2restore = 7000
    nbOfGames = 1000
    player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = network2restore)
    setOfGames(player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def training() :
    nbOfGames = 10
    setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = False)
    player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
    with open("./Saved_Networks/duration-test.ckpt-{}".format(nbOfGames), "w") as f :
        f.write("Duration for {} training games : {}".format(nbOfGames, time.time() - t))

training()
