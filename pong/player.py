#! /usr/bin/python3
# -*- coding: utf-8 -*-

import random
from pynput import keyboard
from pynput.keyboard import Key

class Player :

    def __init__(self, name, isBot) :
        self.name = name
        self.isBot = isBot
        if not self.isBot :
            self.chosenAction = 0
            self.defineKeyboardListener()

        self.initializeProperties()

    def initializeProperties(self) :
        # Constants
        self.learningRate = 0.001
        self.discountFactor = 0.9
        self.explorationRate = 0.999

        # Behaviour when playing & training
        self.trainable = True
        self.exploiting = False
        self.playRandomly = False

        # Statistics
        self.gamesWon = 0
        self.gamesLost = 0

        # Training
        self.statesSequence = []
        self.trainingData = []
        self.maxBatchSize = 10000
        # trainingData will not have more than maxBatchSize elements
        self.miniBatchSize = 32

    def defineKeyboardListener(self) :

        def on_press(key):
            try:
                if key == Key.up :
                    self.chosenAction = 1
                elif key == Key.down :
                    self.chosenAction = 2
                else :
                    self.chosenAction = 0
            except AttributeError:
                self.chosenAction = 0

        def on_release(key):
            self.chosenAction = 0
            if key == keyboard.Key.esc:
                # Stop listener
                return False

        self.listener = keyboard.Listener(on_press = on_press, on_release = on_release)
        self.listener.start()

    def play(self) :
        if self.isBot :
            return random.randint(0,2)
        else :
            return self.chosenAction

    def updateConstants(self, learningRate = None, discountFactor = None, explorationRate = None) :
        if not isinstance(learningRate, type(None)) :
            self.learningRate = learningRate
            # self.createOptimiser()
            # the optimiser must be reinitialised since the learning rate changed
            # self.sess.run(tf.variables_initializer(self.optimiser.variables()))
        if not isinstance(discountFactor, type(None)) :
            self.discountFactor = discountFactor
        if not isinstance(explorationRate, type(None)) :
            self.explorationRate = explorationRate

    def resetStats(self) :
        self.gamesWon = 0
        self.gamesLost = 0

    def updateStats(self, reward) :
        if reward == 1 :
            self.gamesWon += 1
        else :
            self.gamesLost += 1

    def addStateSequence(self, currentState, action, reward, nextState) :
        self.statesSequence.append([currentState, action, reward, nextState])

    def addStateSequence2trainingData(self) :
        self.trainingData = self.trainingData + self.statesSequence
        while len(self.trainingData) > self.maxBatchSize :
            self.trainingData.pop(random.randrange(len(self.trainingData)))
        random.shuffle(self.trainingData)
        self.statesSequence = []
