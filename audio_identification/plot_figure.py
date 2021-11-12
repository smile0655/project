
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np


params = {'legend.fontsize': 'x-large',
          'figure.figsize': (20, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.rcParams.update(params)

music=AudioSegment.from_file("./kikibouba_data/bouba/bouba_0287.wav",format="wav")
#music=AudioSegment.from_file("./queries/queries/Q6.wav",format="wav")
rate=music.frame_rate
print(rate)
width=music.frame_width
print(width)
duration=music.duration_seconds
print(duration)
channel=music.channels
print(channel)
# Convert imported signal to a numeric array, serializing the two chhaels
music_array = np.array(music.get_array_of_samples())
# Normalize array to [-1, 1]
music_array = (music_array / 2**16) * 2
music_array = music_array[int(rate*9.95):int(rate*20.18)]
# Create a time vector in seconds for the whole signal
time = np.linspace(0, len(music_array) / (rate), num=len(music_array))
# print(len(music_array))
#plt.title('bouba_0131.wav(from26.35s to 36.35s)')
plt.title('bouba_0287.wav(from 9.95s to 20.18s)')
plt.xlabel('time(s)')
plt.ylabel('Amplitude')
plt.plot(time,music_array)
plt.show()