from psychopy import visual, core, data, event, logging, sound, gui # import some libraries from PsychoPy
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import time
import re
import math
import time, os

"""
Author: Will Stonehouse
Purpose: This script can flash 2 square waves at any arbitrary frequency superimposed on a video
"""

#function for square wave
def square(frequency,n):
    if math.cos(2*math.pi*frequency*n/60) > 0: #sampling cos is better. 60 is the refresh_rate
        return 0
    else:
        return 1

#function for stimulus
def stimulus():
    
    # ~~~ Input UI ~~~~
    #creating an input box
    modulo = gui.Dlg(title='Left square')
    modulo.addField('Left square in Hz: ')
    modulo.addField('Right square in Hz: ')
    modulo.addField('Duration in Seconds: ')
    modulo.show()

    #store inputs
    refresh_rate=60 #most monitors are 60 Hz
    frequencyL=float(modulo.data[0])
    frequencyR=float(modulo.data[1])
    seconds=int(modulo.data[2])

    #create a window for your stimuli to be presented on
    mywin = visual.Window([1200,800], monitor="testMonitor", units="deg", fullscr=True)

    #create text numbers for countdown
    countdown_1 = visual.TextStim(win=mywin, text='1', pos=[0,0], height=10)
    countdown_2 = visual.TextStim(win=mywin, text='2', pos=[0,0], height=10)
    countdown_3 = visual.TextStim(win=mywin, text='3', pos=[0,0], height=10)

    #drawing the countdown
    for frameN in range(180):
        if frameN < 60:
            countdown_1.draw()
        if frameN >= 60 and frameN < 120:
            countdown_2.draw()
        if frameN >= 120 and frameN < 180:
            countdown_3.draw()
        mywin.update()

    #create some stimuli
    mov = visual.MovieStim3(mywin, filename='train.mp4')
    squareL = visual.GratingStim(win=mywin, mask='circle', size=5, pos=[-14,-6], sf=0, rgb=-1)
    squareR = visual.GratingStim(win=mywin, mask='circle', size=5, pos=[14,-6], sf=0, rgb=-1)
    fixation = visual.TextStim(win=mywin, text='+', pos=[0,0], height=5)

    #prediction feedback
    feedback_L = visual.TextStim(win=mywin, text='Left', pos=[0,5], height=1)
    feedback_R = visual.TextStim(win=mywin, text='Right', pos=[0,5], height=1)
    feedback_B = visual.TextStim(win=mywin, text='Baseline', pos=[0,5], height=1)
    feedback = visual.GratingStim(win=mywin, size=5, pos=[-14,6], sf=0, rgb=-1)

    # Open text file for prediction
    f = open("Result.txt", "r+")

    #stimulus
    for frameN in range(seconds*refresh_rate):
        # Draw movie in the background
        mov.draw()
        
        # Draw Prediction
        f = open("Result.txt", "r+")
        prediction = f.read()
        print(prediction)
        if prediction == '1':
            feedback_L.draw()
        if prediction == '2':
            feedback_R.draw()
        if prediction == '0':
            feedback_B.draw()
            print('Hell Yea')
        f.close()
        
        # Visual Stimulation
        if square(frequencyL,frameN) == 1:
            squareL.draw()
            fixation.draw()
        else:
            fixation.draw()
        if square(frequencyR,frameN) == 1:
            squareR.draw()
            fixation.draw()
        else:
            fixation.draw()
        
        # Refresh screen
        mywin.update()

    #cleanup
    mywin.close()
    core.quit()

'''
f = open("Result.txt","w+")
f.write("0")
f.close()
'''