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

    player.updateConstants(discountFactor = 0.99)
    player.setBehaviour(isTraining)

    with Game(display = display) as game :
        currentStep = 0
        for i in range(nbOfGames) :
            if isTraining :
                player.updateConstants(explorationRate=(0.55 + 0.45 * math.cos(math.pi * i / nbOfGames)))

            done = False
            observations = [game.observation]
            for _ in range(3) :
                observation, reward, done = game.step(player.play(None))
                observations.append(observation)
                currentStep += 1
            while not done:
                action = player.play(observations)
                observation, reward, done = game.step(action)
                previousState = observations[:]
                observations.pop(0)
                observations.append(observation)
                player.addStateSequence(previousState, action, reward, observations)
                player.training(currentStep)
                player.updateStats(reward)
                currentStep += 1
                print(text + "Game : {} ; Step : {} ; Action : {}".format(i+1, currentStep, action))

                if not player.isBot :
                    game.wait()
            player.displayStats()
            player.resetStats()
            game.reset()

nbOfGames = 4
# player.restoreQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)

setOfGames(player = player, isTraining = True, nbOfGames = nbOfGames, display = False)

# player.saveQNetwork("./Saved_Networks/test.ckpt", global_step = nbOfGames)
# with open("./Saved_Networks/duration-test.ckpt-{}".format(nbOfGames), "w") as f :
#     f.write("Duration for {} training games : {}".format(nbOfGames, time.time() - t))
