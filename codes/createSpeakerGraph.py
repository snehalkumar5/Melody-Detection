from scipy.io import wavfile
from scipy import signal

def createSpeakerGraph(currFile):
    intonationStressDir= '../intonation_stress/'
    outDir= '../results/'
    strr = str(intonationStressDir) + str(currFile[:-5]) + '.txt'
    fileID = open(strr,'r')
    dataArray = textscan(fileID, '%f%f%s%f%[^\n\r]', 'Delimiter',' ', 'MultipleDelimsAsOne', true,  'ReturnOnError', false);
    fileID.close()
    nSyls= len(dataArray{4})

    voicedSeg= []
    strr = str(outDir) + str(currFile[:-5]) + '.wav'
    Fs, signal = wavfile.read('../output/audio.wav')
    pch,~,score = swipep(signal,Fs,[75 500],0.01,[],1/20,0.5,0.2)
    if not pch:
        pch = 0
    pch= medfilt1(pch,3) # 10 replaced with 3 here
    pch= 21.4*log10(1+0.00437*pch)

    score= (score-min(score))/range(score)
    nonNanInds= np.where(pch~=0)

    if len(nonNanInds)>3:
        done= 1
        VuV_phns= sign(pch)
        score(pch==0)= NaN
        
        voicedSeg[:,1]= np.where((VuV_phns-[0;VuV_phns(1:end-1)])==1)
        voicedSeg(:,2)= find((VuV_phns-[VuV_phns(2:end);0])==1)
        
        pch= pch-(sum(pch(nonNanInds).*score(nonNanInds))/sum(score(nonNanInds))); pch= pch/range(pch);
        
        
        for iterVoicedSeg= 1:size(voicedSeg,1)
            pch(voicedSeg(iterVoicedSeg,1):voicedSeg(iterVoicedSeg,2))= weightedMedian(pch(voicedSeg(iterVoicedSeg,1):voicedSeg(iterVoicedSeg,2)),score(voicedSeg(iterVoicedSeg,1):voicedSeg(iterVoicedSeg,2)),10);
        end
        pch(1:voicedSeg(1,1)-1)= NaN;
        pch((voicedSeg(size(voicedSeg,1),2)+1):end)= NaN;
        for iterSeg= 2:size(voicedSeg,1)
            pch(voicedSeg(iterSeg-1,2):voicedSeg(iterSeg,1))= interp1([voicedSeg(iterSeg-1,2),voicedSeg(iterSeg,1)],[pch(voicedSeg(iterSeg-1,2)),pch(voicedSeg(iterSeg,1))],linspace(voicedSeg(iterSeg-1,2),voicedSeg(iterSeg,1),voicedSeg(iterSeg,1)-voicedSeg(iterSeg-1,2)+1))';
        end
        pch(nonNanInds(1):nonNanInds(end))= interp1(nonNanInds,pch(nonNanInds),[nonNanInds(1):nonNanInds(end)],'linear');
        
        tic
        [~,~,styPch,~]=dp_weighted_optpolysegsfit(pch(voicedSeg(1,1):voicedSeg(end,2)),nSyls,1,score(voicedSeg(1,1):voicedSeg(end,2)));
        toc
      
        
        save([outDir,currFile(1:end-4)],'styPch');
        
    else
        done= 0
    return done