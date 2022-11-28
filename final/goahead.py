import numpy as np
import os
import scipy.io
import matplotlib.pyplot as plt

def goahead(currFile):
    currFile = currFile[:-4]
    expertGraphDir= '../expertGraphs/'
    speakerGraphDir= '../results/'

    strr = str(expertGraphDir) + str(currFile) + '.mat'
    styPch = scipy.io.loadmat(strr)
    styPch = styPch['styPch']
    styPch = np.array(styPch).astype('float64')


    expertPattern= styPch
    strr = str(speakerGraphDir) + str(currFile) + '.mat'
    while not os.path.exists(strr):
        sleep(0.1)

   
    strr = str(speakerGraphDir) + str(currFile) + '.npy'
    styPch = np.load(strr)
    maxPer= np.max(styPch)
    minPer= np.amin(styPch)
    normPch= 0

    speakerPattern= styPch

    expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
    maxPerEx= np.max(expertPattern)
    minPerEx= np.amin(expertPattern)
    speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
    
    yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
    yticks = sorted(yticks)
    plt.yticks(ticks = yticks, labels = [str(round(t,2)) + 'x' for t in yticks])
    plt.plot(expertPattern, color='blue', label="Expert")
    plt.plot(speakerPattern, color='green', label="Speaker")
    plt.title("What you said (Green)")
    plt.legend(loc="best")
    plt.show()
