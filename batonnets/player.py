#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

class Player :

    def __init__(self, name, isBot, originalNumberSticks) :
        self.name = name
        self.isBot = isBot
        self.QNetwork, self.input = self.createNeuralNetwork(originalNumberSticks)

        self.test([[0,0,0,0]])

    def createNeuralNetwork(self, nbSticks) :
        input = tf.placeholder(tf.float32, shape=[None,4])

        # hidden layer
        W1 = tf.Variable(tf.random_normal([4, 4], stddev=1), name='W1')
        b1 = tf.Variable(tf.random_normal([4]), name='b1')
        hiddenLayer = tf.nn.relu(tf.add(tf.matmul(input,W1), b1))

        # output layer
        W2 = tf.Variable(tf.random_normal([4, 3], stddev=1), name='W2')
        b2 = tf.Variable(tf.random_normal([3]), name="b2")
        output = tf.add(tf.matmul(hiddenLayer, W2), b2)
        return output, input

    def test(self, testData) :
        init = tf.global_variables_initializer()
        with tf.Session() as sess :
            sess.run(init)
            x = sess.run(self.QNetwork, feed_dict={self.input: testData})
            print(x)
