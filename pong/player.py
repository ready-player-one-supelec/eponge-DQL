#! /usr/bin/python3
# -*- coding: utf-8 -*-

import random
from pynput import keyboard
from pynput.keyboard import Key

class Player :

    def __init__(self, name, isBot) :
        self.name = name
        self.isBot = isBot
        self.possibleActions = [0,4,5]
        # respectively doing nothing, going up and going down
        if not self.isBot :
            self.chosenAction = 0
            self.defineKeyboardListener()

    def defineKeyboardListener(self) :

        def on_press(key):
            try:
                if key == Key.up :
                    self.chosenAction = 4
                elif key == Key.down :
                    self.chosenAction = 5
                else :
                    self.chosenAction = 0
            except AttributeError:
                self.chosenAction = 0

        def on_release(key):
            global action
            action = 0
            if key == keyboard.Key.esc:
                # Stop listener
                return False

        self.listener = keyboard.Listener(on_press = on_press, on_release = on_release)
        self.listener.start()

    def play(self) :
        if self.isBot :
            return random.choice(self.possibleActions)
        else :
            return self.chosenAction
