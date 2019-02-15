#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

class ImagePreprocessor :

    def __init__(self, imageSize, sess) :
        self.scope = "processor"
        with tf.variable_scope(self.scope) :
            # input layer
            self.x = tf.placeholder(dtype = tf.uint8, shape = [4, 210, 160, 3])

            self.cropped = tf.image.crop_to_bounding_box(self.x,
                                                            offset_height=35,
                                                            offset_width=0,
                                                            target_height=160,
                                                            target_width=160)
            self.gray = tf.image.rgb_to_grayscale(self.cropped)
            self.resized = tf.image.resize_images(
                self.gray, [imageSize, imageSize], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

            # output layer : image has been properly preprocessed
            self.squeezed = tf.squeeze(self.resized)

            # stacks images on top of each other like a convolutional filter,
            # instead of putting them one after the other
            self.transposed = tf.transpose(self.squeezed, [1, 2, 0])

        self.sess = sess

    def process(self, images) :
        return self.transposed.eval(feed_dict = { self.x: images}, session = self.sess)

class FeatureExtractor:
    def process(self, images):
        res = []
        for image in images:
            im = self._to_gray_scale(image)[34:194, :]
            ball = im == 236
            left_slider = im [:, 16] == 74
            right_slider = im[:, 143] == 92
            res.append([
                *np.unravel_index(ball.argmax(), ball.shape),
                left_slider.argmax(),
                right_slider.argmax()
                ])
        if (res[-1][0], res[-1][1]) != (0, 0) and (res[-2][0], res[-2][1]) != (0, 0):
            direction = (res[-1][0] - res[-2][0], res[-1][1] - res[-2][1])
            norm = (direction[0] **2 + direction[1] **2)**(1/2)
            if norm != 0:
                direction = (direction[0]/norm, direction[1]/norm)
        else:
            direction = (0, 0)
        output = np.array([*direction, *res[-1]], dtype=np.float)
        output[2:] /= 160.0
        return output
    
    @staticmethod
    def _to_gray_scale(im):
        return im[:,:,2]


class DQN :

    def __init__(self, inputSize, scope, miniBatchSize) :

        self.scope = scope
        self.miniBatchSize = miniBatchSize
        with tf.variable_scope(self.scope):
            self.initializeProperties()
            self.createQNetwork(inputSize)
            self.createOptimiser()
        self.saver = tf.train.Saver()

    def initializeProperties(self) :

        self.learningRate = 0.00025
        self.discountFactor = 0.99

    def createQNetwork(self, inputSize) :
        # input layer
        self.x = tf.placeholder(tf.float32, inputSize)
        # expected output placeholder
        self.y = tf.placeholder(tf.float32)

        self._x = tf.cast(self.x, tf.float32)

        self.flatten = tf.layers.flatten(self._x)

        # first dense layer
        self.layer1_dense = tf.layers.dense(self.flatten, 10, activation=tf.nn.tanh)

        # second dense layer
        self.layer2_dense = tf.layers.dense(self.layer1_dense, 16, activation=tf.nn.tanh)

        # output layer
        self.y_before_softmax = tf.layers.dense(self.layer2_dense, 3, activation=tf.nn.tanh)

        self.y_ = tf.nn.softmax(self.y_before_softmax)
        # masked output
        self.actions = tf.placeholder(tf.int32)
        indices = tf.range(self.miniBatchSize) * 3 + self.actions
        self.y_masked = tf.gather(tf.reshape(self.y_before_softmax, [-1]), indices)

        # used to compute the expected output
        self.rewards = tf.placeholder(tf.float32)
        self.zeros = tf.fill([self.miniBatchSize], 0.0)
        self.discountFactorPlaceHolder = tf.constant(self.discountFactor)
        self.expectedOutput = tf.where(tf.not_equal(self.rewards, self.zeros), self.rewards, self.discountFactorPlaceHolder * tf.math.reduce_max(self.y_, axis=1))
        # this filter allows us to ignore the discount factor iff the game is over

        print("Q Network created")

    def createOptimiser(self) :
        # is this loss ?
        self.cost = tf.losses.softmax_cross_entropy(self.y, self.y_masked)
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
