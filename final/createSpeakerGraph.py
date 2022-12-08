from scipy.io import wavfile
import numpy as np
from scipy.ndimage import median_filter
from scipy.interpolate import interp1d
from swipep import swipep
from weightedMedian import weightedMedian
from dp_weighted_optpolysegsfit import dp_weighted_optpolysegsfit
import matplotlib.pyplot as plt

def createSpeakerGraph(currFile):
    intonationStressDir= '../intonation_stress/'
    outDir= '../results/'
    strr = str(intonationStressDir) + str(currFile[:-4]) + '.txt'
    fileID = open(strr,'r')

    dataArray = np.loadtxt(strr, dtype='object',converters={0:float,1:float,2:str,3:float})
    fileID.close()
    nSyls= len(dataArray)

    voicedSeg= []
    strr = str(outDir) + str(currFile[:-4]) + '.wav'
    Fs, signal = wavfile.read(strr)
    signal = signal/32767

    pch,_,score = swipep(signal,Fs,[75, 500],0.01,1.0/96.0,1.0/20.0,0.5,0.2)

    score= (score-np.min(score))/(np.max(score)-np.min(score))
    pch = np.nan_to_num(pch)
    pch = median_filter(pch,3) # 10 replaced with 3 here
    pch = 21.4*np.log10(1+0.00437*pch)
    nonNanInds = np.where(pch!=0)[0]
    if len(nonNanInds)>3:
        done= 1
        VuV_phns = np.sign(pch)
        tmpzero = np.zeros((1,1))
        score[pch==0] = np.NaN
        tmp1 = np.where(VuV_phns-np.vstack((tmpzero,VuV_phns[:-1]))==1)[0]
        tmp1 = np.array([tmp1]).T
        tmp2 = np.where(VuV_phns-np.vstack((VuV_phns[1:],tmpzero))==1)[0]
        tmp2 = np.array([tmp2]).T

        voicedSeg= np.hstack((tmp1,tmp2))
        pch = pch-(np.sum(np.multiply(pch[nonNanInds],score[nonNanInds])/np.sum(score[nonNanInds])))
        pch = pch/(np.max(pch)-np.min(pch))
        for iterVoicedSeg in range(voicedSeg.shape[0]):
            wghtmedout = weightedMedian(pch[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]+1], 
                                                                            score[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]+1], 10).flatten()
            pch[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]+1] = wghtmedout.reshape(wghtmedout.shape[0],1)
        pch[:voicedSeg[0][0]]= np.NaN
        pch[voicedSeg[-1][1]+1:]= np.NaN
        for iterSeg in range(1,voicedSeg.shape[0]):
            a = np.vstack((voicedSeg[iterSeg-1][1],voicedSeg[iterSeg][0])).flatten()
            b = np.vstack((pch[voicedSeg[iterSeg-1][1]],pch[voicedSeg[iterSeg][0]])).flatten()
            fnc = interp1d(a,b)
            ret_fn_interp1d = fnc(np.linspace(voicedSeg[iterSeg-1][1],voicedSeg[iterSeg][0],voicedSeg[iterSeg][0]-voicedSeg[iterSeg-1][1]))
            pch[voicedSeg[iterSeg-1][1]:voicedSeg[iterSeg][0]] = ret_fn_interp1d.reshape(ret_fn_interp1d.shape[0],1)

        func1 = interp1d(nonNanInds.flatten(),pch[nonNanInds].flatten(),'linear')
        tmp1 = np.arange(nonNanInds[0],nonNanInds[-1]+1,1)
        ret_fn1_interp1d = func1(tmp1)
        pch[nonNanInds[0]:nonNanInds[-1]+1]= ret_fn1_interp1d.reshape(ret_fn1_interp1d.shape[0],1)
        _,_,styPch,_ = dp_weighted_optpolysegsfit(pch[voicedSeg[0][0]:voicedSeg[-1][1]+1],nSyls,1,score[voicedSeg[0][0]:voicedSeg[-1][1]+1])
        strr = str(outDir) + str(currFile[:-4])
        np.save(strr,styPch)
        
    else:
        done = 0
    print('done',done)
    return done