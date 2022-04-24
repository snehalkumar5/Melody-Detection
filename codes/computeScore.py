def computeScore(currFile):
    expertGraphDir= '../expertGraphs/'
    speakerGraphDir= '../results/'

    load([expertGraphDir,currFile])
    expertPattern= styPch

    while(~exist([speakerGraphDir,currFile,'.mat'],'file'))
        pause(0.1)
    end

    load([speakerGraphDir,currFile])
    speakerPattern= styPch
    expertPattern(isnan(expertPattern))= []; speakerPattern(isnan(speakerPattern))= [];

    expertDur= length(expertPattern);
    spkrDur= length(speakerPattern);
    chngPer= abs(expertDur-spkrDur)/expertDur;
    if chngPer<0.25:
        [ind1,ind2,~]= dtw(expertPattern',speakerPattern);
        alignSpeakerPattern= speakerPattern(ind2);
        alignExpertPattern= expertPattern(ind1);
        temp= corrcoef(alignSpeakerPattern,alignExpertPattern);
        score= temp(1,2);
    else:
        score= 0

    return score