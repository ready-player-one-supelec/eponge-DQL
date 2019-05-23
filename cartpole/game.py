#! /usr/bin/python3
# -*- coding: utf-8 -*-

import gym
import time
import random

class Game :

    def __init__(self, display = False) :
        self.display = display
        self.observation = None

        # respectively doing nothing, going up and going down
        self.possibleActions = [0, 1]

        self.c = 0

    def __enter__(self) :
        self.env = gym.make('CartPole-v1')
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
            # time.sleep(0.02)
        observation, reward, done, info = self.env.step(self.possibleActions[action])
        self.c += 1
        if done and self.c < 500 :
            reward = -1
        else :
            reward = 1
        self.observation = observation
        return observation, reward, done

    def reset(self) :
        self.observation = self.env.reset()
        self.c = 0

    def random_step(self) :
        return self.step(random.randrange(0,2))
