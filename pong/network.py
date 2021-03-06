#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

class DQN :

    def __init__(self, scope, miniBatchSize) :

        self.scope = scope
        self.miniBatchSize = miniBatchSize
        with tf.variable_scope(self.scope):
            self.initializeProperties()
            self.createQNetwork()
            self.createOptimiser()
        self.saver = tf.train.Saver()

    def initializeProperties(self) :

        self.learningRate = 0.00025
        self.discountFactor = 0.99

    def createQNetwork(self) :
        # input layer
        self.x = tf.placeholder(tf.uint8, [None, 80, 80, 4])
        # expected output placeholder
        self.y = tf.placeholder(tf.float32)

        # first convolutional layer
        self.layer1_conv = tf.layers.conv2d(inputs=self.x / 255,
                                            filters=32,
                                            kernel_size=8,
                                            strides=4,
                                            activation=tf.nn.relu)

        # second convolutional layer
        self.layer2_conv = tf.layers.conv2d(inputs=self.layer1_conv,
                                            filters=64,
                                            kernel_size=4,
                                            strides=2,
                                            activation=tf.nn.relu)

        # third convolutional layer
        self.layer3_conv = tf.layers.conv2d(inputs=self.layer2_conv,
                                            filters=64,
                                            kernel_size=3,
                                            strides=1,
                                            activation=tf.nn.relu)
        self.flattened = tf.layers.flatten(self.layer3_conv)

        # first dense layer
        self.layer1_dense = tf.layers.dense(self.flattened, 512, activation=tf.nn.relu)

        # output layer
        self.y_ = tf.layers.dense(self.layer1_dense, 3)

        # masked output
        self.actions = tf.placeholder(tf.int32)
        indices = tf.range(self.miniBatchSize) * 3 + self.actions
        self.y_masked = tf.gather(tf.reshape(self.y_, [-1]), indices)

        # used to compute the expected output
        self.rewards = tf.placeholder(tf.float32)
        self.zeros = tf.fill([self.miniBatchSize], 0.0)
        self.discountFactorPlaceHolder = tf.constant(self.discountFactor)
        self.expectedOutput = tf.where(tf.not_equal(self.rewards, self.zeros), self.rewards, self.discountFactorPlaceHolder * tf.math.reduce_max(self.y_, axis=1))
        # this filter allows us to ignore the discount factor iff the game is over

        print("Q Network created")

    def createOptimiser(self) :
        # is this loss ?
        self.cost = tf.losses.mean_squared_error(self.y, self.y_masked)
        # Gradient Descent Optimiser definition
        self.optimiser = tf.train.RMSPropOptimizer(self.learningRate, 0.99, 0.0, 1e-6)
        self.train = self.optimiser.minimize(self.cost)
        print("Optimiser created")

    def computeTarget(self, nextStates, rewards) :
        feed_dict = {
            self.x: nextStates,
            self.rewards: rewards
        }
        return self.sess.run(self.expectedOutput, feed_dict = feed_dict)

    def training(self, input, output, actions) :
        feed_dict = { self.x: input,
                    self.y: output,
                    self.actions: actions}
        _, c = self.sess.run([self.train, self.cost], feed_dict=feed_dict)

    def evaluate(self, observations) :
        choice = self.sess.run(self.y_, feed_dict={self.x:[observations]})
        return np.argmax(choice[0])

    def updateConstants(self, learningRate = None) :
        if not isinstance(learningRate, type(None)) :
            self.learningRate = learningRate
            self.createOptimiser()
            # the optimiser must be reinitialised since the learning rate changed
            self.sess.run(tf.variables_initializer(self.optimiser.variables()))

    def saveQNetwork(self, path, global_step) :
        self.saver.save(self.sess, path, global_step = global_step)
        print("Network saved!")

    def restoreQNetwork(self, path, global_step):
        if isinstance(global_step, int) :
            path += "-{}".format(global_step)
        self.saver.restore(self.sess, path)
        print("Network restored!")

    def setSess(self, sess) :
        self.sess = sess
