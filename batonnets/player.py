#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import random

class Player :

    def __init__(self, name, isBot) :
        self.name = name
        self.isBot = isBot

        self.initializeProperties()
        self.createQNetwork()
        self.createOptimiser()
        self.initializeQNetwork()


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

    def createQNetwork(self) :
        # input layer
        self.x = tf.placeholder(tf.float32, [None, 4])
        # expected output placeholder
        self.y = tf.placeholder(tf.float32, [None, 3])

        # first hidden layer
        self.w1 = tf.Variable(tf.random_normal([4, 10], stddev=1), name='W1')
        self.b1 = tf.Variable(tf.random_normal([10]), name='b1')
        self.hiddenLayer1 = tf.nn.relu(tf.add(tf.matmul(self.x, self.w1), self.b1))

        # output layer
        self.wOutput = tf.Variable(tf.random_normal([10, 3], stddev=1), name='Wout')
        self.bOutput = tf.Variable(tf.random_normal([3]), name="bout")
        self.y_ = tf.add(tf.matmul(self.hiddenLayer1, self.wOutput), self.bOutput)

        # choice
        self.choice = 1 + tf.argmax(self.y_, axis=1)

        # masked output
        self.mask = tf.placeholder(tf.float32, (None, 3))
        # mask has 3 values : 1 equals to 1 & the other 2 equal to 0
        self.y_masked = tf.multiply(self.y_, self.mask)

        # used to compute the expected output
        self.rewards = tf.placeholder(tf.float32)
        self.discountFactorPlaceHolder = tf.placeholder(tf.float32)
        # evaluate whether the input is 0000, in which case, the expected output
        # for a transition to 0000 ought to be only the rewards
        # as a matter of fact, the value of the network at 0000 is irrelevant
        # this filter is always 1 unless the input is 0000, in which case, the filter value is 0
        self.filter = 1 - tf.math.reduce_prod(tf.dtypes.cast(tf.equal(self.x, 0 * self.x), tf.float32), axis=1)
        self.expectedOutput = tf.add(self.rewards, self.filter * self.discountFactorPlaceHolder * tf.math.reduce_max(self.y_, axis=1))
        # this filter allows us to ignore the discount factor iff the input is 0000

    def createOptimiser(self) :
        # is this loss ?
        self.cost = tf.losses.mean_squared_error(self.y, self.y_masked)
        # Gradient Descent Optimiser definition
        self.optimiser = tf.train.AdamOptimizer(learning_rate=self.learningRate)
        self.train = self.optimiser.minimize(self.cost)

    def initializeQNetwork(self) :
        # Reinitialise the network according to createQNetwork
        init_op = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init_op)

    def encodeState(self, state) :
        if state >= 0 :
            binaire = bin(state)[2:]
        else :
            binaire = bin(state)[3:]
        encodedState = [int(i) for i in binaire]
        if len(encodedState) < 4 :
            encodedState = [0] * (4 - len(encodedState)) + encodedState
        return encodedState

    def computeAllOutputs(self) :
        allOutputs = []
        actions = []
        rewards = []
        nextStates = []
        for i in range(len(self.trainingData)) :
            state, action, reward, nextState = self.trainingData[i]
            actions.append(action)
            rewards.append(reward)
            nextStates.append(nextState)
        feed_dict={self.x: [self.encodeState(nextState) for nextState in nextStates],
                    self.rewards: rewards,
                    self.discountFactorPlaceHolder: self.discountFactor}
        tmp = self.sess.run(self.expectedOutput, feed_dict=feed_dict)
        for i in range(len(actions)) :
            L = [0] * 3
            L[actions[i] - 1] = tmp[i]
            allOutputs.append(L)
        return allOutputs

    def createMasks(self) :
        masks = []
        for i in range(len(self.trainingData)) :
            mask = [0] * 3
            action = self.trainingData[i][1]
            mask[action - 1] = 1
            masks.append(mask)
        return masks

    def training(self) :
        if not self.trainable :
            return
        nbOfBatches = int(len(self.trainingData) // self.miniBatchSize)
        if len(self.trainingData) % self.miniBatchSize != 0 :
            nbOfBatches += 1
        allOutputs = self.computeAllOutputs()
        allMasks = self.createMasks()
        for i in range(nbOfBatches) :
            beginning = self.miniBatchSize * i
            end = min(self.miniBatchSize * (i + 1), len(self.trainingData))
            input = [self.encodeState(transition[0]) for transition in self.trainingData[beginning : end]]
            # Input refers to the actual state
            output = allOutputs[beginning : end]
            masks = allMasks[beginning : end]
            feed_dict = {self.x:input, self.y: output, self.mask: masks}
            _, c = self.sess.run([self.train, self.cost], feed_dict=feed_dict)

    def updateConstants(self, learningRate, discountFactor, explorationRate) :
        if not isinstance(learningRate, type(None)) :
            self.learningRate = learningRate
            self.createOptimiser()
            # the optimiser must be reinitialised since the learning rate changed
            self.sess.run(tf.variables_initializer(self.optimiser.variables()))
        if not isinstance(discountFactor, type(None)) :
            self.discountFactor = discountFactor
        if not isinstance(explorationRate, type(None)) :
            self.explorationRate = explorationRate

    def play(self, currentNumberSticks) :
        if self.isBot :
            if not self.playRandomly and (self.exploiting or random.random() > self.explorationRate) :
                encodedState = self.encodeState(currentNumberSticks)
                action = self.sess.run(self.choice, feed_dict={self.x: [encodedState]})[0]
            else :
                action = random.randint(1,3)
        else :
            ask = True
            while ask :
                action = input("Choose action: ")
                try :
                    action = int(action)
                except :
                    ask = True
                else :
                    if 0 < action <= 3 :
                        ask = False
        return action

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

    def correctStateSequence(self, reward, nextState) :
        if len(self.statesSequence) != 0 :
            self.statesSequence[-1][-2:] = [reward, nextState]

    def addStateSequence2trainingData(self) :
        self.trainingData = self.trainingData + self.statesSequence
        while len(self.trainingData) > self.maxBatchSize :
            self.trainingData.pop(random.randrange(len(self.trainingData)))
        random.shuffle(self.trainingData)
        self.statesSequence = []
