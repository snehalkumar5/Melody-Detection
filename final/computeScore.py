from time import sleep
import numpy as np
from dtw import dtw
import os
import scipy.io

def computeScore(currFile):
    currFile = currFile[:-4]
    expertGraphDir= '../expertGraphs/'
    speakerGraphDir= '../results/'

    strr = str(expertGraphDir) + str(currFile) + '.mat'
    styPch = scipy.io.loadmat(strr)
    styPch = styPch['styPch']
    styPch = np.array(styPch).astype('float64')
    
    expertPattern= styPch
    strr = str(speakerGraphDir) + str(currFile) + '.npy'
    styPch = np.load(strr)

    speakerPattern= styPch

    expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
    speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
    
    expertDur= len(expertPattern)
    spkrDur= len(speakerPattern)
    chngPer= abs(expertDur-spkrDur)/expertDur
    if chngPer<0.3:
        ind1,ind2,_= dtw(expertPattern,speakerPattern)
        alignSpeakerPattern = speakerPattern[ind2]
        alignExpertPattern = expertPattern[ind1]
        temp= np.corrcoef(alignSpeakerPattern,alignExpertPattern)
        score= temp[0][1]
    else:
        score= 0
    
    return score