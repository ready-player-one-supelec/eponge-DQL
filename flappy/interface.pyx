#! /usr/bin/python3
# -*- coding:utf-8 -*-

cimport cython

cdef extern from "flappy.h":
    void reset_flappy()
    void init_flappy(int display)
    void exit_flappy()
    void run_flappy()
    int step_flappy(int movement)

def init(display) :
    cdef int c_display = display;
    init_flappy(c_display)

def exit() :
    exit_flappy()

def game_step(movement) :
    cdef int c_movement = movement
    cdef int c_continuer
    c_continuer = step_flappy(c_movement)
    return c_continuer
