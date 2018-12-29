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
    game.reset()
    return players

nbSticks = 12
learningRate = 0.01
discountFactor = 0.9
explorationRate = 0.999

game = Game(nbSticks)
player = Player("Toto", True)
player.updateConstants(None, None, 0.5)
player2 = Player("Joueur", False)

players = Players(player, player2)

gameMaster(game, players)
