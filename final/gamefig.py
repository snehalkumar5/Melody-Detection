from computeScore import computeScore
from createSpeakerGraph import createSpeakerGraph
from goahead import goahead
from scipy.io import wavfile

def start():
    spkrfile = input('Enter speaker audio file:')
    done = createSpeakerGraph(spkrfile)
    if done == 0:
        score = 0
    else:
        score = computeScore(spkrfile)
    print('score:',score)
    # if score<0.01:
    #     while score < 0.01:
    #         print("Score too low, please try again")
    #         spkrfile = input("Enter new speaker audio file:")
    #         done = createSpeakerGraph(spkrfile)
    #         if done == 0:
    #             score = 0
    #         else:
    #             score = computeScore(spkrfile)
    # else:
    goahead(spkrfile)

start()