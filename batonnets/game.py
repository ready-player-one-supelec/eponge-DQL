#! /usr/bin/python3
# -*- coding: utf-8 -*-

class Game :

    def __init__(self, numberSticks) :
        self.currentNumberSticks = numberSticks
        self.originalNumberSticks = numberSticks

    def reset(self) :
        self.currentNumberSticks = self.originalNumberSticks

    def display(self, playerName) :
        print("There are currently {} sticks. It's {}'s turn".format(self.currentNumberSticks, playerName))

    def isOver(self) :
        return self.currentNumberSticks <= 0

    def move(self, action) :
        self.currentNumberSticks -= action
        reward = -1 if self.isOver() else 0
        return reward
