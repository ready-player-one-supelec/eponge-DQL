#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import random
import time
from pynput import keyboard
from pynput.keyboard import Key
from network import DQN, ImagePreprocessor


class Player :

    def __init__(self, name, isBot) :
        self.name = name
        self.isBot = isBot
        if not self.isBot :
            self.chosenAction = 0
            self.defineKeyboardListener()

        self.initializeProperties()
        self.QNetwork = DQN(self.imageSize, "QN", self.miniBatchSize)
        self.TDTarget = DQN(self.imageSize, "TD", self.miniBatchSize)
        self.sess = tf.Session()
        self.QNetwork.setSess(self.sess)
        self.TDTarget.setSess(self.sess)
        self.processor = ImagePreprocessor(self.imageSize, self.sess)
        self.sess.run(tf.global_variables_initializer())
        self.synchronise()

    def initializeProperties(self) :
        # Q Network Constants
        self.imageSize = 80
        self.synchronisationPeriod = 10000

        # Constants
        self.explorationRate = 0.999

        # Behaviour when playing & training
        self.trainable = True
        self.exploiting = False

        # Statistics
        self.gamesWon = 0
        self.gamesLost = 0

        # Training
        self.trainingData = []
        self.maxBatchSize = 1000000
        # trainingData will not have more than maxBatchSize elements
        self.miniBatchSize = 32
        self.miniBatch = []
        self.startTraining = 50000
        # the training will happen iff we have more than startTraining data in trainingData

        print("Properties initialized")

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

    def training(self, step) :
        if not self.trainable or len(self.trainingData) < self.startTraining:
            return
        if step % self.synchronisationPeriod == 0 :
            self.synchronise()
        self.miniBatch = random.sample(self.trainingData, self.miniBatchSize)
        states, actions, rewards, nextStates = zip(*self.miniBatch)
        output = self.TDTarget.computeTarget(nextStates, rewards)
        self.QNetwork.training(states, output, actions)

    def play(self) :
        if self.isBot :
            if self.exploiting or random.random() > self.explorationRate :
                return self.QNetwork.evaluate(self.buffer)
            else :
                return random.randrange(0,3)
        else :
            return self.chosenAction

    def updateConstants(self, learningRate = None, explorationRate = None) :
        self.QNetwork.updateConstants(learningRate)
        if not isinstance(explorationRate, type(None)) :
            self.explorationRate = explorationRate

    def resetStats(self) :
        self.gamesWon = 0
        self.gamesLost = 0

    def updateStats(self, reward) :
        if reward == 1 :
            self.gamesWon += 1
        elif reward == -1 :
            self.gamesLost += 1

    def displayStats(self) :
        # print("{} victories & {} defeats".format(self.gamesWon, self.gamesLost))
        print(self.gamesWon, self.gamesLost)

    def addStateSequence(self, action, reward, nextState) :
        nS = self.processor.process(nextState)
        self.trainingData.append([self.buffer, action, reward, nS])
        self.buffer = nS
        while len(self.trainingData) > self.maxBatchSize :
            self.trainingData.pop(0)

    def saveQNetwork(self, path, global_step = None) :
        self.QNetwork.saveQNetwork(path, global_step)

    def restoreQNetwork(self, path, global_step = None):
        self.QNetwork.restoreQNetwork(path, global_step)

    def setBehaviour(self, isTraining) :
        self.trainable = isTraining
        self.exploiting = not isTraining

    def synchronise(self):
        e1_params = [t for t in tf.trainable_variables() if t.name.startswith(self.QNetwork.scope)]
        e1_params = sorted(e1_params, key=lambda v: v.name)
        e2_params = [t for t in tf.trainable_variables() if t.name.startswith(self.TDTarget.scope)]
        e2_params = sorted(e2_params, key=lambda v: v.name)

        update_ops = []
        for e1_v, e2_v in zip(e1_params, e2_params):
            op = e2_v.assign(e1_v)
            update_ops.append(op)
        self.sess.run(update_ops)
