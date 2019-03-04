#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random
import math
import time
import os

t = time.time()
player = Player(name = "Toto", isBot = True)


def setOfGames(player, isTraining, nbOfGames, display) :
    # isTraining = True for a training session, False for a test session
    text = "TRAINING ; " if isTraining else "PLAYING ; "

    global imagesPipe, actionsPipe

    player.setBehaviour(isTraining)
    imagesPipe = os.open("images",  os.O_RDONLY)#, encoding="ISO-8859-1")
    actionsPipe = open("actions",  "wb")# encoding="ISO-8859-1")

    actionsPipe.write(b'01')
    actionsPipe.write(b'00')
    actionsPipe.write(b'10')
    tmp = os.read(imagesPipe,2)
    print(tmp.decode("utf-8"))

    with Game(display = display) as game :
        pass
        # currentStep = 0
        # for i in range(nbOfGames) :
        #     if isTraining :
        #         player.updateConstants(explorationRate= 1 - 0.9 * i / nbOfGames)
        #
        #     done = False
        #     observations = [game.observation]
        #     for _ in range(3) :
        #         observation, reward, done = game.random_step()
        #         observations.append(observation)
        #         currentStep += 1
        #     player.buffer = player.processor.process(observations)
        #     while not done:
        #         action = player.play()
        #         observation, reward, done = game.step(action)
        #         observations.pop(0)
        #         observations.append(observation)
        #         player.addStateSequence(action, reward, observations)
        #         player.training(currentStep)
        #         player.updateStats(reward)
        #         currentStep += 1
        #
        #     print(text + "Game : {} ; Step : {}".format(i+1, currentStep))
        #     player.displayStats()
        #     player.resetStats()
        #     game.reset()

    actionsPipe.write(b'11');
    actionsPipe.close()
    tmp = os.read(imagesPipe, 2)
    while b'11' not in tmp :
        time.sleep(0.1)
        print(tmp)
        tmp += os.read(imagesPipe, 2)
    os.close(imagesPipe)

def testing(display = False) :
    network2restore = 7000
    nbOfGames = 1000
    player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = network2restore)
    setOfGames(player = player, isTraining = False, nbOfGames = nbOfGames, display = display)

def training() :
    nbOfGames = 10
    setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = False)
    player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
    print("\n{}\n".format(time.time() - t))

training()
