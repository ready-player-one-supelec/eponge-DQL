#! /usr/bin/python3
# -*- coding: utf-8 -*-

import dill as pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


X = pickle.load(open("results", "rb"))

t = X['Time']
hour = t // 3600
minutes = (t // 60) % 60
strTime = ''
if hour > 0 :
    strTime += "{:.0f}h ".format(hour)
strTime += "{:.0f}m".format(minutes)

Y = X['Results']
n = len(Y)
abscisse = [Y[0][j]['Epoch'] for j in range(len(Y[0]))]

for i in range(len(Y)) :
    for j in range(len(Y[i])) :
        steps_survived = []
        victory_strike = []
        for oneTest in Y[i][j]['Results'] :
            steps_survived.append(oneTest['Steps survived'])
            victory_strike.append(oneTest['Victory strike'])
        Y[i][j] = [np.mean(steps_survived), np.max(victory_strike)]

Y = np.transpose(Y, (1, 0, 2))
mean = np.mean(Y, axis = 1)
std = np.std(Y, axis = 1)
confidence = 1.96 * std / np.sqrt(n)

mean_steps = []
mean_strike = []
conf_steps = []
conf_strike = []

for e in mean :
    mean_steps.append(e[0])
    mean_strike.append(e[1])

for e in confidence :
    conf_steps.append(e[0])
    conf_strike.append(e[1])


plt.xlim(0, abscisse[-1])
plt.ylim(0, 500)
plt.xlabel('Training games')
plt.ylabel('Average of steps survived')
plt.title('Survival of Q-Learning AI in CartPole environment')

line1, = plt.plot(abscisse, mean_steps, 'b-', label='Real curve')
line2, = plt.plot([0, 1500], [195, 195], 'y-', label='Victory Threshold')
plt.errorbar(abscisse, mean_steps, conf_steps, color="red", linestyle="None")
first_legend = plt.legend(handles=[line1, line2], loc='upper right')
plt.gca().add_artist(first_legend)

handles = []
handles.append(mpatches.Patch(color='none', label='Number of runs : %d' % n))
handles.append(mpatches.Patch(color='none', label='Confidence level : 95%'))
handles.append(mpatches.Patch(color='none', label='Duration of simulation : ' + strTime))
handles.append(mpatches.Patch(color='none', label='Number of test games for each point : %d' % X['Number of testing games']))
handles.append(mpatches.Patch(color='none', label='Learning Rate : {}'.format(X['Learning Rate'])))
handles.append(mpatches.Patch(color='none', label='Discount Factor : {}'.format(X['Discount Factor'])))
handles.append(mpatches.Patch(color='none', label='Memory size : %d steps' % X['Replay memory']))
handles.append(mpatches.Patch(color='none', label='Synchronisation period : %d steps' % X['Synchronisation period']))
plt.legend(handles=handles, loc='upper left')

plt.show()
