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
                player.updateConstants(explorationRate= 1 - 0.9 * i / nbOfGames)

            done = False
            observations = [game.observation]
            for _ in range(3) :
                observation, reward, done = game.random_step()
                observations.append(observation)
                currentStep += 1
            player.buffer = player.processor.process(observations)
            while not done:
                if not player.isBot :
                    game.wait()
                action = player.play()
                observation, reward, done = game.step(action)
                observations.pop(0)
                observations.append(observation)
                player.addStateSequence(action, reward, observations)
                player.training(currentStep)
                player.updateStats(reward)
                currentStep += 1

            print(text + "Game : {} ; Step : {}".format(i+1, currentStep))
            player.displayStats()
            player.resetStats()
            game.reset()

nbOfGames = 4
# player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)

setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = False)

# player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
# with open("./Saved_Networks/duration-test.ckpt-{}".format(nbOfGames), "w") as f :
#     f.write("Duration for {} training games : {}".format(nbOfGames, time.time() - t))
