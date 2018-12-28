#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import random

class Player :

    def __init__(self, name, isBot) :
        self.name = name
        self.isBot = isBot
        self.learningRate = 0
        self.discountFactor = 0
        self.explorationRate = 0
        self.trainable = True
        self.exploiting = False
        self.playRandomly = False

        self.createQNetwork()
        self.createOptimiser()
        self.initializeQNetwork()


    def createQNetwork(self) :
        # input layer
        self.x = tf.placeholder(tf.float32, [None, 4])
        # expected output placeholder
        self.y = tf.placeholder(tf.float32, [None, 3])

        # hidden layer
        self.w1 = tf.Variable(tf.random_normal([4, 4], stddev=1), name='W1')
        self.b1 = tf.Variable(tf.random_normal([4]), name='b1')
        self.hiddenLayer = tf.nn.relu(tf.add(tf.matmul(self.x, self.w1), self.b1))

        # output layer
        self.w2 = tf.Variable(tf.random_normal([4, 3], stddev=1), name='W2')
        self.b2 = tf.Variable(tf.random_normal([3]), name="b2")
        self.y_ = tf.add(tf.matmul(self.hiddenLayer, self.w2), self.b2)

    def createOptimiser(self) :
        # is this loss ?
        self.cost = tf.losses.mean_squared_error(self.y, self.y_)
        # Gradient Descent Optimiser definition
        self.optimiser = tf.train.GradientDescentOptimizer(learning_rate=self.learningRate).minimize(self.cost)

    def initializeQNetwork(self) :
        # Reinitialise the network according to createQNetwork
        init_op = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init_op)

    def predict(self, input) :
        prediction = self.sess.run(self.y_, feed_dict={self.x: input})
        return prediction

    def train(self, input, output, epochs=1000) :
        for i in range(epochs) :
            _, c = self.sess.run([self.optimiser, self.cost], feed_dict={self.x:input, self.y: output})
            print("Cost is ", c)

    def updateConstants(self, learningRate, discountFactor, explorationRate) :
        if not isinstance(learningRate, type(None)) :
            self.learningRate = learningRate
        if not isinstance(discountFactor, type(None)) :
            self.discountFactor = discountFactor
        if not isinstance(explorationRate, type(None)) :
            self.explorationRate = explorationRate

    def play(self, currentNumberSticks) :
        if self.isBot :
            if not self.playRandomly and (self.exploiting or random.random() > self.explorationRate) :
                encodedState = [int(i) for i in bin(currentNumberSticks)[2:]]
                action = 1 + self.sess.run(tf.argmax(self.predict([encodedState])[0]))
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
