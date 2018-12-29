#! /usr/bin/python3
# -*- coding: utf-8 -*-

from player import *

class Players :

    def __init__(self, player1, player2) :
        self.player1 = player1
        self.player2 = player2


    def __getitem__(self, key) :
        if key == 0 :
            return self.player1
        if key == 1 :
            return self.player2
        raise IndexError

    def addStateSequence2trainingData(self) :
        self.player1.addStateSequence2trainingData()
        self.player2.addStateSequence2trainingData()

    def updateStats(self, winnerID) :
        self[winnerID].updateStats(1)
        self[1 - winnerID].updateStats(-1)

    def updateConstants(self, learningRate=None, discountFactor=None, explorationRate=None) :
        self.player1.updateConstants(learningRate, discountFactor, explorationRate)
        self.player2.updateConstants(learningRate, discountFactor, explorationRate)

    def resetStats(self) :
        self.player1.resetStats()
        self.player2.resetStats()

    def train(self) :
        self.player1.train()
        self.player2.train()

    def displayStats(self) :
        print("{} won {} times out of {} games".format(self[0].name, self[0].gamesWon, self[0].gamesWon + self[0].gamesLost))
        print("{} won {} times out of {} games".format(self[1].name, self[1].gamesWon, self[1].gamesWon + self[1].gamesLost))
