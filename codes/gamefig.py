from codes.computeScore import computeScore
from codes.createSpeakerGraph import createSpeakerGraph

def start():
    spkrfile = input('Etner spkr file')
    done = createSpeakerGraph(spkrfile)
    if done == 0:
        score=0
    else:
        score = computeScore(spkrfile)
    