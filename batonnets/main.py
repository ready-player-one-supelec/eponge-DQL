#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import *
from player import *

nbSticks = 12
learningRate = 0.01
discountFactor = 0.9
explorationRate = 0.999

game = Game(nbSticks)
player = Player("Toto", True)
player.updateConstants(None, None, 0.5)
for i in range(10) :
    a = player.play(12)
    print(a)
