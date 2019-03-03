#! /usr/bin/python3
# -*- coding:utf-8 -*-

from interface import *
import random
import matplotlib.pyplot as plt

init(1)

plt.figure()
plt.ion()
plt.show()

continuer = True
while continuer :
    m = random.randint(0, 100)
    m = int(m >= 97)
    continuer, image, reward = game_step(m)
    # print(list(image))
    exit_game()
    exit()
    plt.imshow(image, cmap="gray", aspect="equal")
    print(len(image), len(image[0]))
    plt.draw()
    input()

exit_game()
