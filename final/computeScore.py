from time import sleep
import numpy as np
from dtw import dtw
import os

def computeScore(currFile):
    expertGraphDir= '../expertGraphs/'
    speakerGraphDir= '../results/'

    # load([expertGraphDir,currFile])
    strr = str(expertGraphDir) + str(currFile)
    with open(strr,'r') as f:
        styPch = f.readlines()
    
    expertPattern= styPch
    strr = str(speakerGraphDir) + str(currFile) + '.mat'
    while not os.path.exists(strr):
        sleep(0.1)

    strr = str(speakerGraphDir) + str(currFile)
    with open(strr,'r') as f:
        styPch = f.readlines()
    # load([speakerGraphDir,currFile])
    speakerPattern= styPch

    expertPattern = np.nan_to_num(expertPattern)
    speakerPattern = np.nan_to_num(speakerPattern)

    expertDur= len(expertPattern)
    spkrDur= len(speakerPattern)
    chngPer= abs(expertDur-spkrDur)/expertDur
    if chngPer<0.25:
        ind1,ind2,_= dtw(expertPattern,speakerPattern)
        alignSpeakerPattern= speakerPattern(ind2)
        alignExpertPattern= expertPattern(ind1)
        temp= np.corrcoef(alignSpeakerPattern,alignExpertPattern)
        score= temp[0][1]
    else:
        score= 0
        
    return score