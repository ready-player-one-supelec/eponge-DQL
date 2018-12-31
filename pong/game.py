#! /usr/bin/python3
# -*- coding: utf-8 -*-

import gym
import time

class Game :

    def __init__(self, display = False) :
        self.display = display

    def __enter__(self) :
        self.env = gym.make('Pong-v0')
        self.env.reset()
        return self

    def __exit__(self, type, value, traceback) :
        self.env.env.close()

    def step(self, action, display = None) :
        if isinstance(display, type(None)) :
            display = self.display
        assert(isinstance(display, bool))
        if self.display :
            self.env.render()
        return self.env.step(action)

    def wait(self) :
        time.sleep(0.05)
