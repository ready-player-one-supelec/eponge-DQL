#! /usr/bin/python3
# -*- coding:utf-8 -*-

cimport cython

cdef extern from "flappy.h":
    void reset_flappy()
    unsigned char* init_flappy(int display)
    void exit_flappy()
    void run_flappy()
    int step_flappy(int movement, int *reward)
    void treatingImage(unsigned char *image)
    void getSize(int *x_size, int *y_size)

cdef unsigned char* image = NULL;
cdef int X_SIZE = 0;
cdef int Y_SIZE = 0;

import time

def init(display) :
    global image
    cdef int c_display = display
    image = init_flappy(c_display)
    getSize(&X_SIZE, &Y_SIZE)
    print(X_SIZE, Y_SIZE)

def exit() :
    exit_flappy()

def convertImage() :
    py_image = [[0 for j in range(X_SIZE)] for i in range(Y_SIZE)]
    for i in range(X_SIZE) :
        for j in range(Y_SIZE) :
            py_image[j][i] = image[j * X_SIZE + i]
    return py_image

def game_step(movement) :
    cdef int reward;
    cdef int c_movement = movement
    cdef int c_continuer
    c_continuer = step_flappy(c_movement, &reward)
    treatingImage(image)
    t = time.time()
    convertImage()
    print(time.time() - t)
    return c_continuer, convertImage(), reward
