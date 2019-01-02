#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import random
from pynput import keyboard
from pynput.keyboard import Key

class ImagePreprocessor :

    def __init__(self, imageSize) :
        # input layer
        self.x = tf.placeholder(tf.float32, [4, 210, 160, 3])

        self.cropped = tf.image.crop_to_bounding_box(self.x,
                                                        offset_height=35,
                                                        offset_width=0,
                                                        target_height=160,
                                                        target_width=160)
        self.gray = tf.image.rgb_to_grayscale(self.cropped) / 255
        self.resized = tf.image.resize_images(
            self.gray, [imageSize, imageSize], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

        # output layer : image has been properly preprocessed
        self.squeezed = tf.squeeze(self.resized)

        # stacks images on top of each other like a convolutional filter,
        # instead of putting them one after the other
        self.transposed = tf.transpose(self.squeezed, [1, 2, 0])

    def process(self, sess, images) :
        return sess.run(self.transposed, feed_dict = { self.x: images})

class Player :

    def __init__(self, name, isBot) :
        self.name = name
        self.isBot = isBot
        if not self.isBot :
            self.chosenAction = 0
            self.defineKeyboardListener()

        self.initializeProperties()
        self.processor = ImagePreprocessor(self.imageSize)
        self.createQNetwork()
        self.createOptimiser()
        self.initializeQNetwork()

    def initializeProperties(self) :
        # Q Network Constants
        self.imageSize = 80

        # Constants
        self.learningRate = 0.001
        self.discountFactor = 0.9
        self.explorationRate = 0.999

        # Behaviour when playing & training
        self.trainable = True
        self.exploiting = False

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
        self.x = tf.placeholder(tf.float32, [None, self.imageSize, self.imageSize, 4])
        # expected output placeholder
        self.y = tf.placeholder(tf.float32, [None, 3])

        # first convolutional layer
        self.layer1_conv = tf.layers.conv2d(inputs=self.x,
                                            filters=32,
                                            kernel_size=8,
                                            strides=4,
                                            activation=tf.nn.relu,
                                            padding="same")
        self.layer1_conv = tf.layers.max_pooling2d(inputs=self.layer1_conv,
                                                    pool_size=2,
                                                    strides=2,
                                                    padding="same")

        # second convolutional layer
        self.layer2_conv = tf.layers.conv2d(inputs=self.layer1_conv,
                                            filters=64,
                                            kernel_size=4,
                                            strides=2,
                                            activation=tf.nn.relu,
                                            padding="same")
        self.layer2_conv = tf.layers.max_pooling2d(inputs=self.layer2_conv,
                                                    pool_size=2,
                                                    strides=2,
                                                    padding="same")

        # third convolutional layer
        self.layer3_conv = tf.layers.conv2d(inputs=self.layer2_conv,
                                            filters=64,
                                            kernel_size=3,
                                            strides=1,
                                            activation=tf.nn.relu,
                                            padding="same")
        self.layer3_conv = tf.layers.max_pooling2d(inputs=self.layer3_conv,
                                                    pool_size=2,
                                                    strides=2,
                                                    padding="same")

        self.flattened = tf.layers.flatten(self.layer3_conv)

        # first dense layer
        self.w1 = tf.Variable(tf.random_normal([256, 256], stddev=1), name='W1')
        self.b1 = tf.Variable(tf.random_normal([256]), name='b1')
        self.layer1_dense = tf.nn.relu(tf.add(tf.matmul(self.flattened, self.w1), self.b1))

        # output layer
        self.wOutput = tf.Variable(tf.random_normal([256, 3], stddev=1), name='Wout')
        self.bOutput = tf.Variable(tf.random_normal([3]), name="bout")
        self.y_ = tf.add(tf.matmul(self.layer1_dense, self.wOutput), self.bOutput)

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
        self.optimiser = tf.train.RMSPropOptimizer(learning_rate=self.learningRate)
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
            nextStates.append(self.processor.process(self.sess,nextState))
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
            input = [self.processor.process(self.sess, transition[0]) for transition in self.trainingData[beginning : end]]
            # Input refers to the actual state
            output = allOutputs[beginning : end]
            masks = allMasks[beginning : end]
            feed_dict = { self.x: input,
                        self.y: output,
                        self.mask: masks}
            _, c = self.sess.run([self.train, self.cost], feed_dict=feed_dict)

    def play(self, observations = None) :
        if self.isBot :
            if not isinstance(observations, type(None)) and (self.exploiting or random.random() > self.explorationRate) :
                y_, choice = self.sess.run([self.y_, self.choice], feed_dict={self.x:[self.processor.process(self.sess, observations)]})
                # print(y_)
                return choice[0]
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
        if self.trainable :
            self.statesSequence.append([currentState, action, reward, nextState])

    def addStateSequence2trainingData(self) :
        if self.trainable :
            self.trainingData = self.trainingData + self.statesSequence
            while len(self.trainingData) > self.maxBatchSize :
                self.trainingData.pop(random.randrange(len(self.trainingData)))
            self.statesSequence = []
            random.shuffle(self.trainingData)

    def saveQNetwork(self, path, global_step = None) :
        self.saver.save(self.sess, path, global_step = global_step)
        print("Network saved!")

    def restoreQNetwork(self, path, global_step = None):
        if isinstance(global_step, int) :
            path += "-{}".format(global_step)
        self.saver.restore(self.sess, path)
        print("Network restored!")

    def setBehaviour(self, isTraining) :
        if isTraining :
            self.exploiting = False
            self.trainable = True
        else :
            self.exploiting = True
            self.trainable = False
