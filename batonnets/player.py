#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

class Player :

    def __init__(self, name, isBot, learning_rate) :
        self.name = name
        self.isBot = isBot
        self.learningRate = learning_rate

        self.createQNetwork()
        self.createOptimiser()
        self.initializeQNetwork()

        print(self.predict([[0.25, 0.5, 0.75, 1]]))
        self.train([[0.25, 0.5, 0.75, 1]], [[0,0.25,0.5]])
        print(self.predict([[0.25, 0.5, 0.75, 1]]))

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
