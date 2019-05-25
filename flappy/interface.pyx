#! /usr/bin/python3
# -*- coding:utf-8 -*-

cimport cython
import numpy as np
from libc.stdlib cimport malloc, free

cdef extern from "flappy.h":
    void reset_flappy(int difficulty)
    char* init_flappy(int display, int difficulty)
    void exit_flappy()
    void run_flappy()
    int step_flappy(int movement, float *reward)
    void treatingImage(char *image)
    void getSize(int *x_size, int *y_size)
    void updateFeatures(int *xToPipe, float *yToUpperPipe, float *yToLowerPipe, float *vy, float *yToTop, float *yToBottom)


cdef class Game :

    cdef public char* image
    cdef public int X_SIZE, Y_SIZE
    cdef public int c_display, xToPipe
    cdef public float yToUpperPipe, yToLowerPipe, vy, yToTop, yToBottom, reward
    cdef public int c_movement, c_continuer, returnFeatures
    cdef public int difficulty

    def __init__(self, display, returnFeatures, difficulty) :
        self.c_display = display
        self.returnFeatures = returnFeatures
        self.difficulty = difficulty
        getSize(&self.X_SIZE, &self.Y_SIZE)

    def __enter__(self) :
        self.image = init_flappy(self.c_display, self.difficulty)
        self.image[self.X_SIZE * self.Y_SIZE] = 0
        return self

    def __exit__(self,  type, value, traceback) :
        free(self.image)
        exit_flappy()

    def convertImage(self) :
        tmp = np.fromstring(self.image, np.uint8)
        tmp = np.reshape(tmp, [self.Y_SIZE, self.X_SIZE])
        return tmp

    def reset(self) :
        reset_flappy(self.difficulty)

    def game_step(self, movement) :
        self.c_movement = movement
        self.c_continuer = step_flappy(self.c_movement, &self.reward)
        if self.returnFeatures :
            updateFeatures(&self.xToPipe, &self.yToUpperPipe, &self.yToLowerPipe, &self.vy, &self.yToTop, &self.yToBottom)
            retour = np.zeros(6)
            retour[0] = self.xToPipe
            retour[1] = self.yToUpperPipe
            retour[2] = self.yToLowerPipe
            retour[3] = self.vy
            retour[4] = self.yToTop
            retour[5] = self.yToBottom
        else :
            treatingImage(self.image)
            retour = self.convertImage()
        if self.c_continuer == 0 :
            self.reset()
        return retour, self.reward, 1 - self.c_continuer
