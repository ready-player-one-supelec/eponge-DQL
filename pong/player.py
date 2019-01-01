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
        self.maxBatchSize = 1500
        # trainingData will not have more than maxBatchSize elements
        self.miniBatchSize = 32

        print("Properties initialized")

    def createQNetwork(self) :
        # input layer
        self.x = tf.placeholder(tf.float32, [None, 210,160,3])
        # expected output placeholder
        self.y = tf.placeholder(tf.float32, [None, 3])

        self.cropped_x = tf.image.crop_to_bounding_box(self.x,
                                                        offset_height=35,
                                                        offset_width=0,
                                                        target_height=160,
                                                        target_width=160)
        self.gray_x = tf.image.rgb_to_grayscale(self.cropped_x) / 255

        # first convolutional layer
        self.layer1_conv = tf.layers.conv2d(inputs=self.gray_x,
                                            filters=16,
                                            kernel_size=8,
                                            strides=4,
                                            activation=tf.nn.relu)
        self.layer1_conv = tf.layers.max_pooling2d(inputs=self.layer1_conv,
                                                    pool_size=2,
                                                    strides=2)

        # second convolutional layer
        self.layer2_conv = tf.layers.conv2d(inputs=self.layer1_conv,
                                            filters=32,
                                            kernel_size=4,
                                            strides=2,
                                            activation=tf.nn.relu)
        self.layer2_conv = tf.layers.max_pooling2d(inputs=self.layer2_conv,
                                                    pool_size=2,
                                                    strides=2)

        self.flattened = tf.layers.flatten(self.layer2_conv)

        # first dense layer
        self.w1 = tf.Variable(tf.random_normal([512, 100], stddev=1), name='W1')
        self.b1 = tf.Variable(tf.random_normal([100]), name='b1')
        self.layer1_dense = tf.nn.relu(tf.add(tf.matmul(self.flattened, self.w1), self.b1))

        # second dense layer
        self.w2 = tf.Variable(tf.random_normal([100, 10], stddev=1), name='W2')
        self.b2 = tf.Variable(tf.random_normal([10]), name='b2')
        self.layer2_dense = tf.nn.relu(tf.add(tf.matmul(self.layer1_dense, self.w2), self.b2))

        # output layer
        self.wOutput = tf.Variable(tf.random_normal([10, 3], stddev=1), name='Wout')
        self.bOutput = tf.Variable(tf.random_normal([3]), name="bout")
        self.y_ = tf.add(tf.matmul(self.layer2_dense, self.wOutput), self.bOutput)

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
        self.saver = tf.train.Saver()
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
        feed_dict={self.x: nextStates,
                    self.rewards: rewards,
                    self.discountFactorPlaceHolder: self.discountFactor}
        tmp = self.sess.run(self.expectedOutput, feed_dict=feed_dict)
        for i in range(len(actions)) :
            L = [0] * 3
            L[actions[i]] = tmp[i]
            allOutputs.append(L)
        return allOutputs

    def createMasks(self) :
        masks = []
        for i in range(len(self.trainingData)) :
            mask = [0] * 3
            action = self.trainingData[i][1]
            mask[action] = 1
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
            input = [transition[0] for transition in self.trainingData[beginning : end]]
            # Input refers to the actual state
            output = allOutputs[beginning : end]
            masks = allMasks[beginning : end]
            feed_dict = {self.x:input, self.y: output, self.mask: masks}
            _, c = self.sess.run([self.train, self.cost], feed_dict=feed_dict)

    def play(self, observation) :
        if self.isBot :
            if not self.playRandomly and (self.exploiting or random.random() > self.explorationRate) :
                print(self.sess.run(self.y_, feed_dict={self.x:[observation]})[0])
                return self.sess.run(self.choice, feed_dict={self.x: [observation]})[0]
            else :
                return random.randrange(0,3)
        else :
            return self.chosenAction

    def updateConstants(self, learningRate = None, discountFactor = None, explorationRate = None) :
        if not isinstance(learningRate, type(None)) :
            self.learningRate = learningRate
            self.createOptimiser()
            # the optimiser must be reinitialised since the learning rate changed
            self.sess.run(tf.variables_initializer(self.optimiser.variables()))
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
        elif reward == -1 :
            self.gamesLost += 1

    def displayStats(self) :
        # print("{} victories & {} defeats".format(self.gamesWon, self.gamesLost))
        print(self.gamesWon, self.gamesLost)

    def addStateSequence(self, currentState, action, reward, nextState) :
        self.statesSequence.append([currentState, action, reward, nextState])

    def addStateSequence2trainingData(self) :
        self.trainingData = self.trainingData + self.statesSequence
        while len(self.trainingData) > self.maxBatchSize :
            self.trainingData.pop(random.randrange(len(self.trainingData)))
        random.shuffle(self.trainingData)
        self.statesSequence = []

    def saveQNetwork(self, path, global_step = None) :
        self.saver.save(self.sess, path, global_step = global_step)
        print("Network saved!")

    def restoreQNetwork(self, path, global_step = None):
        if isinstance(global_step, int) :
            path += "-{}".format(global_step)
        self.saver.restore(self.sess, path)
        print("Network restored!")
