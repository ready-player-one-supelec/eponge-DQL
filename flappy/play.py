#! /usr/bin/python3
# -*- coding:utf-8 -*-

from interface import *
import random

init(1)

continuer = True
while continuer :
    m = random.randint(0, 100)
    m = int(m >= 97)
    continuer = game_step(m)

exit()
