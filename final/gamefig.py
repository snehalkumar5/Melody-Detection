from time import sleep
from computeScore import computeScore
from createSpeakerGraph import createSpeakerGraph
from scipy.io import wavfile
import os

def start():
    spkrfile = input('Enter speaker audio file:')
    done = createSpeakerGraph(spkrfile)
    if done == 0:
        score = 0
    else:
        score = computeScore(spkrfile)
    print('score:',score)
    # if score<0.01:
    #     set(handles.figure1,'visible','off')
    #     k= waitforbuttonpress
    #     close(gcf)
    #     set(handles.figure1,'visible','on')
    #     strr = '../wav/' + str(handles.sysFileName) + '.wav'
    #     fs, y = wavfile.read(strr)
    #     y= (y/(max(abs(y))))*0.99
    # sleep(1.5)
    # os.system(y, fs)

start()