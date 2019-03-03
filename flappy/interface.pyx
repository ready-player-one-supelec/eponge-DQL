#! /usr/bin/python3
# -*- coding:utf-8 -*-

cimport cython
cimport numpy as np
import numpy as np
import time

cdef extern from "flappy.h":
    void reset_flappy()
    char* init_flappy(int display)
    void exit_flappy()
    void run_flappy()
    int step_flappy(int movement, int *reward)
    void treatingImage(char *image)
    void getSize(int *x_size, int *y_size)

cdef char* image = NULL
cdef int X_SIZE = 0
cdef int Y_SIZE = 0
getSize(&X_SIZE, &Y_SIZE)

def init(display) :
    global image
    cdef int c_display = display
    image = init_flappy(c_display)
    print(X_SIZE, Y_SIZE)

def exit_game() :
    exit_flappy()

def convertImage() :
    image[X_SIZE * Y_SIZE - 1] = 0
    return np.fromstring(image, np.uint8)

def game_step(movement) :
    cdef int reward;
    cdef int c_movement = movement
    cdef int c_continuer
    c_continuer = step_flappy(c_movement, &reward)
    treatingImage(image)
    return c_continuer, convertImage(), reward
