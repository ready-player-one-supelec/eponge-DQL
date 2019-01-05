#! /usr/bin/python3
# -*- coding: utf-8 -*-

import tensorflow as tf

class ImagePreprocessor :

    def __init__(self, imageSize, sess) :
        self.scope = "processor"
        with tf.variable_scope(self.scope) :
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

        self.sess = sess

    def process(self, images) :
        return self.transposed.eval(feed_dict = { self.x: images}, session = self.sess)


class DQN :

    def __init__(self, imageSize, scope, miniBatchSize) :

        self.scope = scope
        self.miniBatchSize = miniBatchSize
        with tf.variable_scope(self.scope):
            self.initializeProperties()
            self.createQNetwork(imageSize)
            self.createOptimiser()
        self.saver = tf.train.Saver()

    def initializeProperties(self) :

        self.learningRate = 0.00025
        self.discountFactor = 0.99

    def createQNetwork(self, imageSize) :
        # input layer
        self.x = tf.placeholder(tf.float32, [None, imageSize, imageSize, 4])
        # expected output placeholder
        self.y = tf.placeholder(tf.float32)

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
        self.actions = tf.placeholder(tf.int32)
        batch_nums = tf.range(0, limit=self.miniBatchSize)
        indices = tf.stack((batch_nums, self.actions), axis=1) # the axis is the dimension number
        self.y_masked = tf.gather_nd(self.y_, indices)

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
        self.optimiser = tf.train.RMSPropOptimizer(self.learningRate, 0.99, 0.0, 1e-6)
        self.train = self.optimiser.minimize(self.cost)
        print("Optimiser created")

    def computeTarget(self, nextStates, rewards) :
        feed_dict = {
            self.x: nextStates,
            self.rewards: rewards,
            self.discountFactorPlaceHolder: self.discountFactor
        }
        return self.sess.run(self.expectedOutput, feed_dict = feed_dict)

    def training(self, input, output, actions) :
        feed_dict = { self.x: input,
                    self.y: output,
                    self.actions: actions}
        _, c = self.sess.run([self.train, self.cost], feed_dict=feed_dict)

    def evaluate(self, observations) :
        y_, choice = self.sess.run([self.y_, self.choice], feed_dict={self.x:[observations]})
        # print(y_)
        return choice[0]

    def updateConstants(self, learningRate = None, discountFactor = None) :
        if not isinstance(discountFactor, type(None)) :
            self.discountFactor = discountFactor
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