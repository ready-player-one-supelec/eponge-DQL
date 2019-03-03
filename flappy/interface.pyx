#! /usr/bin/python3
# -*- coding:utf-8 -*-

cimport cython

cdef extern from "flappy.h":
    void reset_flappy()
    char* init_flappy(int display)
    void exit_flappy()
    void run_flappy()
    int step_flappy(int movement)
    void treatingImage(char *image)
    void getSize(int *x_size, int *y_size)

cdef char* image = NULL;
cdef int X_SIZE = 0;
cdef int Y_SIZE = 0;

def init(display) :
    global image
    cdef int c_display = display
    image = init_flappy(c_display)
    getSize(&X_SIZE, &Y_SIZE)

def exit() :
    exit_flappy()

def game_step(movement) :
    cdef int c_movement = movement
    cdef int c_continuer
    c_continuer = step_flappy(c_movement)
    treatingImage(image)
    return c_continuer
