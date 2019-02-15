#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random
import math
import time

def setOfGames(player, isTraining, nbOfGames, display) :
    # isTraining = True for a training session, False for a test session
    stats = []
    text = "TRAINING ; " if isTraining else "PLAYING ; "

    player.setBehaviour(isTraining)

    with Game(display = display) as game :
        currentStep = 0
        for i in range(nbOfGames) :
            if isTraining :
                player.updateConstants(explorationRate= 1 - 0.75 * i / nbOfGames)

            done = False
            observations = [game.observation]
            for _ in range(3) :
                observation, reward, done = game.random_step()
                observations.append(observation)
                currentStep += 1
            player.buffer = player.processor.process(observations)
            while not done:
                action = player.play()
                observation, reward, done = game.step(action)
                observations.pop(0)
                observations.append(observation)
                player.addStateSequence(action, reward, observations)
                player.training(currentStep)
                player.updateStats(reward)
                currentStep += 1

            print(text + "Game : {} ; Step : {}".format(i+1, currentStep))
            stats.append(player.getStats())
            player.displayStats()
            player.resetStats()
            game.reset()
    return stats

def test(filePath, step, nbOfGames, display = False) :
    player = Player(name = "Toto", isBot=True)
    player.restoreQNetwork(filePath, global_step = step)
    return setOfGames(player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def train(filePath, nbOfGames, last_step = 0) :
    t = time.time()
    player = Player(name = "Toto", isBot = True)
    if last_step != 0:
        player.restoreQNetwork(filePath, global_step = last_step)
    setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = False)
    player.saveQNetwork(filePath, global_step = last_step + nbOfGames)
    with open(filePath + "{}duration".format(last_step + nbOfGames), "w") as f :
        f.write("Duration for {} training games : {}".format(nbOfGames, time.time() - t))
