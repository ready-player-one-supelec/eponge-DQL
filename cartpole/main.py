#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random
import math
import time
import dill as pickle
from multiprocessing import Pool


t = time.time()
# player = Player(name = "Toto", isBot = True)

def setOfGames(run, player, isTraining, nbOfGames, display) :
    # isTraining = True for a training session, False for a test session
    text = "Run {} ; ".format(run) if run != 0 else ""
    text += "TRAINING ; " if isTraining else "PLAYING ; "

    player.setBehaviour(isTraining)

    victoryCounter = 0
    if isTraining :
        history_of_results = []

    with Game(display = display) as game :
        currentStep = 0
        results = []
        for i in range(1, nbOfGames + 1) :
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

            print(text + "Game : {} ; Step : {}".format(i, currentStep))
            # player.displayStats()
            if player.gamesWon >= 195 :
                victoryCounter += 1
            else :
                victoryCounter = 0
            results.append({
                'Game number' : i,
                'Steps survived' : player.gamesWon + 1,
                'Victory strike' : victoryCounter
            })
            player.resetStats()
            game.reset()
            # if victoryCounter >= 100 :
            #     break
            if isTraining and i % 10 == 0 :
                history_of_results.append({
                    'Epoch' : i,
                    'Results' : testing(run, player, False)
                })
    if not isTraining :
        return results
    else :
        return history_of_results


def testing(run, player, display = False) :
    network2restore = 1000
    nbOfGames = 150
    # player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = network2restore)
    return setOfGames(run = run, player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def training(run, player) :
    nbOfGames = 1000
    results = setOfGames(run = run, player = player, isTraining = True, nbOfGames = nbOfGames, display = False)
    # player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
    # with open("./Saved_Networks/duration-test.ckpt-{}".format(nbOfGames), "w") as f :
    #     f.write("Duration for {} training games : {}".format(nbOfGames, time.time() - t))
    return results

def doUrStuff(run) :
    player = Player(name = str(run), isBot = True)
    res = training(run, player)
    del player
    return res

def multicoreCartPole() :
    # Number of processors
    processors = 70
    # Number of runs (for the average)
    runs = 70

    pool = Pool(processes = processors)

    times = [(i,) for i in range(1, runs + 1)]
    X = pool.starmap(doUrStuff, tuple(times))
    t2 = time.time() - t
    print(t2)
    pickle.dump({
        "Results" : X,
        "Time" : t2
        }, open("results", "wb"))

# testing(player)
# training(player)
multicoreCartPole()
