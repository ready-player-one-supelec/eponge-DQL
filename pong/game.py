#! /usr/bin/python3
# -*- coding: utf-8 -*-

import gym
import time
import random

class Game :

    def __init__(self, display = False) :
        self.display = display
        self.observation = None

        self.possibleActions = [0,4,5]
        # respectively doing nothing, going up and going down

    def __enter__(self) :
        self.env = gym.make('Pong-v0')
        self.reset()
        return self

    def __exit__(self, type, value, traceback) :
        self.env.env.close()

    def step(self, action, display = None) :
        if isinstance(display, type(None)) :
            display = self.display
        assert(isinstance(display, bool))
        if self.display :
            self.env.render()
        observation, reward, done, info = self.env.step(self.possibleActions[action])
        self.observation = observation
        return observation, reward, done

    def reset(self) :
        self.observation = self.env.reset()

    def random_step(self) :
        return self.step(random.randrange(0,3))
