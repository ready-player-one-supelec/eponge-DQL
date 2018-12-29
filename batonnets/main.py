#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
from players import Players

import random

def gameMaster(game, players) :
    currentPlayer = random.randint(0,1)
    while not game.isOver() :
        currentState = game.currentNumberSticks
        if not players[currentPlayer].isBot :
            game.display(players[currentPlayer].name)
        action = players[currentPlayer].play(currentState)
        reward = game.move(action)
        players[currentPlayer].addStateSequence(currentState, action, reward, game.currentNumberSticks)
        currentPlayer = 1 - currentPlayer
        players[currentPlayer].correctStateSequence(-reward, game.currentNumberSticks)
    players.updateStats(currentPlayer) # the current player at this moment is the winner
    players.addStateSequence2trainingData()
    game.reset()
    return players

def setOfGames(nbGames, game, players, learningRate, discountFactor, explorationRateTable) :
    players.updateConstants(learningRate=learningRate, discountFactor=discountFactor)
    for i in range(nbGames) :
        print("PLAYING ", i)
        players.updateConstants(explorationRate=explorationRateTable[i])
        gameMaster(game, players)
    return players


nbSticks = 12
learningRate = 0.01
discountFactor = 0.9
explorationRateInit = 0.999
explorationRateMin = 0.1

game = Game(nbSticks)
player = Player("Toto", True)
player2 = Player("Joueur", True)
players = Players(player, player2)

nbGames = 5000
explorationRateTable = [max(explorationRateInit ** i, explorationRateMin) for i in range(nbGames)]

for i in range(100) :
    print("training : ", i)
    setOfGames(50, game, players, learningRate, discountFactor, explorationRateTable[50 * i : 50 * (i+1)])
    players.train()

for i in range(1,13) :
    print("----------")
    print("i = ", i)
    print(player.sess.run(player.y_, feed_dict={player.x: [player.encodeState(i)]}))
    print("----------")
