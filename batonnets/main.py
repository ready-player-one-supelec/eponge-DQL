#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import *
from player import *

nbSticks = 12
learningRate = 0.01
game = Game(nbSticks)
player = Player("Toto", True, learningRate)
