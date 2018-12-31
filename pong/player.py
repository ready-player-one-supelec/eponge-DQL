#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
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

        print("Properties initialized")

    def createQNetwork(self) :
        # input layer
        self.x = tf.placeholder(tf.float32, [None, 210,160,3])
        # expected output placeholder
        self.y = tf.placeholder(tf.float32, [None, 3])

        self.flattened_x = tf.contrib.layers.flatten(self.x)

        # first hidden layer
        self.w1 = tf.Variable(tf.random_normal([100800, 10], stddev=1), name='W1')
        self.b1 = tf.Variable(tf.random_normal([10]), name='b1')
        self.hiddenLayer1 = tf.nn.relu(tf.add(tf.matmul(self.flattened_x, self.w1), self.b1))

        # output layer
        self.wOutput = tf.Variable(tf.random_normal([10, 3], stddev=1), name='Wout')
        self.bOutput = tf.Variable(tf.random_normal([3]), name="bout")
        self.y_ = tf.add(tf.matmul(self.hiddenLayer1, self.wOutput), self.bOutput)

        # choice
        self.choice = tf.argmax(self.y_, axis=1)

        # masked output
        self.mask = tf.placeholder(tf.float32, (None, 3))
        # mask has 3 values : 1 equals to 1 & the other 2 equal to 0
        self.y_masked = tf.multiply(self.y_, self.mask)

        # used to compute the expected output
        self.rewards = tf.placeholder(tf.float32)
        self.discountFactorPlaceHolder = tf.placeholder(tf.float32)
        self.filter = tf.dtypes.cast(tf.equal(self.rewards, 0 * self.rewards), tf.float32)
        self.expectedOutput = tf.add(self.rewards, self.filter * self.discountFactorPlaceHolder * tf.math.reduce_max(self.y_, axis=1))
        # this filter allows us to ignore the discount factor iff the game is over

        print("Q Network created")

    def createOptimiser(self) :
        # is this loss ?
        self.cost = tf.losses.mean_squared_error(self.y, self.y_masked)
        # Gradient Descent Optimiser definition
        self.optimiser = tf.train.AdamOptimizer(learning_rate=self.learningRate)
        self.train = self.optimiser.minimize(self.cost)
        print("Optimiser created")

    def initializeQNetwork(self) :
        # Reinitialise the network according to createQNetwork
        init_op = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init_op)
        print("Variables initialized")


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

    def play(self, observation) :
        if self.isBot :
            if not self.playRandomly and (self.exploiting or random.random() > self.explorationRate) :
                return self.sess.run(self.choice, feed_dict={self.x: [observation]})[0]
            else :
                return random.randrange(0,3)
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
