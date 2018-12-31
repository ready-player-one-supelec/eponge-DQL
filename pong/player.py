#! /usr/bin/python3
# -*- coding: utf-8 -*-

import random

class Player :

    def __init__(self, name, isBot) :
        self.name = name
        self.isBot = isBot
        self.possibleActions = [0,4,5]
        # respectively doing nothing, going up and going down

    def play(self) :
        return random.choice(self.possibleActions)
