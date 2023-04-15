import matplotlib.pyplot as plt # veri görselleştirme
import numpy as np #diziler ile işlem yapmak icin

from os.path import dirname, join as pjoin
from scipy.io import wavfile
from scipy.signal import resample #ses tonu için
import scipy.io

samplerate, data = wavfile.read("C:/rise_teknoloji/robot.wav") #ses dosyasını okuma 

#göreselleitirme
print(data[:, 0])
length = data.shape[0]
time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
