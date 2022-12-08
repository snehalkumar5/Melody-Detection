# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# Sampling frequency
freq = 16000

# Recording duration
duration = 2

# Start recorder with the given values
# of duration and sample frequency
recording = sd.rec(int(duration * freq),
				samplerate=freq, channels=1)

# Record audio for the given number of seconds
sd.wait()

c = np.reshape(np.array(recording,dtype=np.float16),(1,recording.shape[0]))

print(c.shape)
# This will convert the NumPy array to an audio
# file with the given sampling frequency
write("recording0.wav", freq, recording)


# Convert the NumPy array to audio file
