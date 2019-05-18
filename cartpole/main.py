#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random
import math
import time
import sys
import dill as pickle

# Number of runs (for the average)
runs = 1

t = time.time()
player = Player(name = "Toto", isBot = True)

def setOfGames(player, isTraining, nbOfGames, display) :
    # isTraining = True for a training session, False for a test session
    text = "TRAINING ; " if isTraining else "PLAYING ; "

    player.setBehaviour(isTraining)

    victoryCounter = 0
    if isTraining :
        history_of_results = []

    with Game(display = display) as game :
        currentStep = 0
        results = []
        for i in range(nbOfGames) :
            result = {'Game number' : i+1}
            if isTraining :
                tmp = 1 - 0.95 * i / nbOfGames
                if tmp > 0.1 :
                    player.updateConstants(explorationRate= tmp)
                else :
                    player.updateConstants(explorationRate= 0.1)

            done = False
            player.buffer = game.observation
            while not done:
                action = player.play()
                observation, reward, done = game.step(action)
                player.addStateSequence(action, reward, observation)
                player.training(currentStep)
                player.updateStats(reward)
                currentStep += 1

            print(text + "Game : {} ; Step : {}".format(i+1, currentStep))
            player.displayStats()
            if player.gamesWon >= 195 :
                victoryCounter += 1
            else :
                victoryCounter = 0
            result['Steps survived'] = player.gamesWon + 1
            result['Victory strike'] = victoryCounter
            results.append(result)
            player.resetStats()
            game.reset()
            # if victoryCounter >= 100 :
            #     break
            if isTraining and (i+1) % 10 == 0 :
                history_of_results.append({
                    'Epoch' : i + 1,
                    'Results' : testing(player, False)
                })
    if not isTraining :
        return results
    else :
        return history_of_results


def testing(player, display = False) :
    network2restore = 1000
    nbOfGames = 10
    # player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = network2restore)
    return setOfGames(player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def training(player) :
    nbOfGames = 100
    results = setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = False)
    # player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
    # with open("./Saved_Networks/duration-test.ckpt-{}".format(nbOfGames), "w") as f :
    #     f.write("Duration for {} training games : {}".format(nbOfGames, time.time() - t))
    return results


# testing(player)
# training(player)
X = [training(Player(name = str(i), isBot = True)) for i in range(1, runs + 1)]
pickle.dump(X, open("results{}".format(sys.argv[1]), "wb"))
