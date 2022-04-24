from scipy.io import wavfile
import numpy as np
from scipy.signal import medfilt
from scipy.interpolate import interp1d
from swipep import swipep
from weightedMedian import weightedMedian
from dp_weighted_optpolysegsfit import dp_weighted_optpolysegsfit

def createSpeakerGraph(currFile):
    # currFile = '1a.wav'
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

    pch,_,score = swipep(signal,Fs,[75, 500],0.01,[],1/20,0.5,0.2)
    pch = np.nan_to_num(pch)
    pch= medfilt(pch,3) # 10 replaced with 3 here
    pch= 21.4*np.log10(1+0.00437*pch)

    score= (score-np.min(score))/(np.max(score)-np.min(score))
    nonNanInds= np.where(pch!=0)[0]

    if len(nonNanInds)>3:
        done= 1
        VuV_phns= np.sign(pch)
        
        score[pch==0]= np.NaN
        tmp1 = np.where(VuV_phns-np.hstack((0,VuV_phns[:-1]))==1)[0]
        tmp1 = np.array([tmp1]).T
        tmp2 = np.where(VuV_phns-np.hstack((VuV_phns[1:],0))==1)[0]
        tmp2 = np.array([tmp2]).T

        voicedSeg= np.hstack((tmp1,tmp2))
        
        pch= pch-(np.sum(np.dot(pch[nonNanInds],score[nonNanInds])/np.sum(score[nonNanInds])))
        pch= pch/np.ptp(pch)
        
        for iterVoicedSeg in voicedSeg.shape[0]:
            pch[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]] = weightedMedian(pch[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]], 
                                                                            score[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]], 10)

        pch[:voicedSeg[0][0]-1]= np.NaN
        pch[voicedSeg[voicedSeg.shape[0]][1]+1:]= np.NaN
        for iterSeg in range(1,voicedSeg.shape[0]):
            fnc = interp1d([voicedSeg[iterSeg-1][1],voicedSeg[iterSeg][0]],[pch[voicedSeg[iterSeg-1][1]],pch(voicedSeg(iterSeg,1))])
            ret_fn_interp1d = fnc(np.linspace(voicedSeg[iterSeg-1][1],voicedSeg[iterSeg][0],voicedSeg[iterSeg][0]-voicedSeg[iterSeg-1][1]+1))
            pch[voicedSeg[iterSeg-1][1]:voicedSeg[iterSeg][0]] = ret_fn_interp1d

        func1 = interp1d(nonNanInds,pch[nonNanInds],'linear')
        tmp1 = np.linspace(nonNanInds[0],nonNanInds[-1])
        ret_fn1_interp1d = func1(tmp1)
        pch[nonNanInds[0]:nonNanInds[-1]]= ret_fn1_interp1d
        
        _,_,styPch,_ = dp_weighted_optpolysegsfit(pch[voicedSeg[0][0]:voicedSeg[-1][1]],nSyls,1,score[voicedSeg[0][0]:voicedSeg[-1][1]])

        strr = str(outDir) + str(currFile[:-4])
        with open(strr,'w') as f:
            f.write(styPch)
        
    else:
        done = 0
    return done

createSpeakerGraph('114.wav')