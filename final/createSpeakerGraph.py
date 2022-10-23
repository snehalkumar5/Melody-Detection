from scipy.io import wavfile
import numpy as np
from scipy.signal import medfilt
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
    # print('swipep return size:',pch.shape,"score:",score.shape)
    # for i in pch:
        # print(i)
    # print("score:")
    for i in score:
        print(i)
    score= (score-np.min(score))/(np.max(score)-np.min(score))
    pch = np.nan_to_num(pch)
    pch= medfilt(pch,3) # 10 replaced with 3 here
    pch= 21.4*np.log10(1+0.00437*pch)
    # plt.plot(pch)
    # plt.show()
    nonNanInds= np.where(pch!=0)[0]
    # print('len',len(nonNanInds))
    if len(nonNanInds)>3:
        done= 1
        VuV_phns= np.sign(pch)
        
        score[pch==0]= np.NaN
        tmp1 = np.where(VuV_phns-np.hstack((0,VuV_phns[:-1]))==1)[0]
        tmp1 = np.array([tmp1]).T
        tmp2 = np.where(VuV_phns-np.hstack((VuV_phns[1:],0))==1)[0]
        tmp2 = np.array([tmp2]).T

        voicedSeg= np.hstack((tmp1,tmp2))
        # print(voicedSeg, voicedSeg.shape)
        pch= pch-(np.sum(np.dot(pch[nonNanInds],score[nonNanInds])/np.sum(score[nonNanInds])))
        pch= pch/np.ptp(pch)
        # pch = np.reshape(pch,(pch.shape[0],1))
        for iterVoicedSeg in range(voicedSeg.shape[0]):
            print(iterVoicedSeg)
            pch[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]] = weightedMedian(pch[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]], 
                                                                            score[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]], 10).flatten()
        # print('weighted done')
        # print(pch,voicedSeg,nonNanInds,nSyls,score)
        pch[:voicedSeg[0][0]-1]= np.NaN
        pch[voicedSeg[-1][1]:]= np.NaN
        for iterSeg in range(1,voicedSeg.shape[0]):
            a = np.vstack((voicedSeg[iterSeg-1][1],voicedSeg[iterSeg][0])).flatten()
            b = np.vstack((pch[voicedSeg[iterSeg-1][1]],pch[voicedSeg[iterSeg][0]])).flatten()
            print(a.shape,b.shape)
            fnc = interp1d(a,b)
            ret_fn_interp1d = fnc(np.linspace(voicedSeg[iterSeg-1][1],voicedSeg[iterSeg][0],voicedSeg[iterSeg][0]-voicedSeg[iterSeg-1][1]))
            pch[voicedSeg[iterSeg-1][1]:voicedSeg[iterSeg][0]] = ret_fn_interp1d

        func1 = interp1d(nonNanInds,pch[nonNanInds],'linear')
        tmp1 = np.linspace(nonNanInds[0],nonNanInds[-1], nonNanInds[-1]-nonNanInds[0])
        ret_fn1_interp1d = func1(tmp1)
        pch[nonNanInds[0]:nonNanInds[-1]]= ret_fn1_interp1d
        # print('pch',pch)
        _,_,styPch,_ = dp_weighted_optpolysegsfit(pch[voicedSeg[0][0]:voicedSeg[-1][1]],nSyls,1,score[voicedSeg[0][0]:voicedSeg[-1][1]])
        # print('MAAAAAAAA',styPch)
        strr = str(outDir) + str(currFile[:-4])
        with open(strr,'w') as f:
            f.write(styPch)
        
    else:
        done = 0
    print('done',done)
    return done

# createSpeakerGraph('227.wav')