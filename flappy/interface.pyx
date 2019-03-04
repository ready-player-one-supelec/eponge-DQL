#! /usr/bin/python3
# -*- coding:utf-8 -*-

cimport cython
cimport numpy as np
import numpy as np

cdef extern from "flappy.h":
    void reset_flappy()
    char* init_flappy(int display)
    void exit_flappy()
    void run_flappy()
    int step_flappy(int movement, int *reward)
    void treatingImage(char *image)
    void getSize(int *x_size, int *y_size)
    void updateFeatures(int *xToPipe, float *yToUpperPipe, float *yToLowerPipe, float *vy, float *yToTop, float *yToBottom)

cdef char* image = NULL
cdef int X_SIZE = 0
cdef int Y_SIZE = 0
getSize(&X_SIZE, &Y_SIZE)

def init(display) :
    global image
    cdef int c_display = display
    image = init_flappy(c_display)
    image[X_SIZE * Y_SIZE] = 0

def exit_game() :
    exit_flappy()

def convertImage() :
    tmp = np.fromstring(image, np.uint8)
    tmp = np.reshape(tmp, [Y_SIZE, X_SIZE])
    return tmp

def game_step(movement, returnFeatures) :
    # return features is a boolean
    cdef int reward, xToPipe
    cdef float yToUpperPipe, yToLowerPipe, vy, yToTop, yToBottom
    cdef int c_movement = movement
    cdef int c_continuer
    c_continuer = step_flappy(c_movement, &reward)
    if returnFeatures :
        updateFeatures(&xToPipe, &yToUpperPipe, &yToLowerPipe, &vy, &yToTop, &yToBottom)
        return c_continuer, np.array([xToPipe, yToUpperPipe, yToLowerPipe, vy, yToTop, yToBottom]), reward
    else :
        treatingImage(image)
        return c_continuer, convertImage(), reward
