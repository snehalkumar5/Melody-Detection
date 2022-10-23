import numpy as np
from swipep_0 import swipep
import audioread
import scipy.signal
from scipy.interpolate import interp1d
from weightedMedian import weightedMedian
from dp_weighted_optpolysegsfit import dp_weighted_optpolysegsfit

wavDir= '../wav/'
intonationStressDir= '../intonation_stress/'
outDir= '../expertGraphs/'

def extractPatterns():
    fileList= dir([wavDir,'*.wav'])
    for iterFile in range(len(fileList)):
        if iterFile!=190:
            currFile= fileList(iterFile).name
            fnam = intonationStressDir + currFile[:-5]+'.txt'
            fileID = open(fnam,'r')
            dataArray = np.loadtxt(fileID, delimiter=' ',dtype={'names':('col1','col2','col3','col4'), 'formats': ('float','float','S4','float')})
            fileID.close()
            nSyls= len(dataArray['col4'])
            
            voicedSeg= np.array([])
            fnam = wavDir + currFile[:-5] + '.wav'
            signal,Fs= audioread(fnam)
            pch,timeLocs,score = swipep(signal,Fs,np.array([75,500]),0.01,[],1/20,0.5,0.2)
            if not pch:
                pch=0
            pch= scipy.signal.medfilt(pch) # 10 replaced with 3 here
            pch= 21.4*np.log10(1+0.00437*pch)
            
            score = (score-min(score))/range(score)
            nonNanInds = np.argwhere(pch!=0)[0]
            VuV_phns = np.sign(pch)
            score[pch==0] = np.NaN
            
            styPch= pch
            
            voicedSeg[:,0]= np.argwhere((VuV_phns-np.vstack((0,VuV_phns[:-2]))==1))[0]
            voicedSeg[:,1]= np.argwhere((VuV_phns-np.vstack((VuV_phns[2:],0))==1))[0]
            
            pch= pch-(np.sum(np.multiply(pch(nonNanInds),score(nonNanInds)))/np.sum(score(nonNanInds)))
            pch= pch/range(pch)            
            
            for iterVoicedSeg in range(voicedSeg.shape[0]):
                pch[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]]= weightedMedian(pch[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]],score[voicedSeg[iterVoicedSeg][0]:voicedSeg[iterVoicedSeg][1]],10)
            pch[:voicedSeg[0][0]-1]= np.NaN
            pch[voicedSeg[voicedSeg.shape[0]][1]+1:]= np.NaN
            for iterSeg in range(1,voicedSeg.shape[0]):
                pch[voicedSeg[iterSeg-1][1]:voicedSeg[iterSeg][0]]= interp1d([voicedSeg[iterSeg-1][1],voicedSeg[iterSeg][0]],[pch[voicedSeg[iterSeg-1][1]],pch[voicedSeg[iterSeg][0]]],np.linspace(voicedSeg[iterSeg-1][1],voicedSeg[iterSeg][0],voicedSeg[iterSeg][0]-voicedSeg[iterSeg-1][1]+1))

            pch[nonNanInds[0]:nonNanInds[-1]]= interp1d(nonNanInds,pch[nonNanInds],np.arange(nonNanInds[0],nonNanInds[-1]),'linear')
            styPch[:-1]= np.NaN
            
            _,_,styPch[voicedSeg[0][0]:voicedSeg[-1][2]],_ = dp_weighted_optpolysegsfit(pch[voicedSeg[0][0]:voicedSeg[-1][1]],nSyls,1,score[voicedSeg[0][0]:voicedSeg[-1][1]])
            fname = outDir + currFile[:-5]
            fd = open(fname,'w')
            fd.write('styPch')
            fd.close()
        