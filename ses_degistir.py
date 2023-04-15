import matplotlib.pyplot as plt # ->görselleştirme
from scipy.io import wavfile #dosya
from scipy.signal import resample, butter, filtfilt #filtreler



samplerate, data = wavfile.read("C:/rise_teknoloji/enkhoca.wav") # Ses dosyasını yükleme

# ses sinayline ayar vererek tonu değiştir
nyquist_freq = 0.6 * samplerate
cutoff_freq = 600.0 # Hz
order = 5
cutoff = cutoff_freq / nyquist_freq
b, a = butter(order, cutoff, btype="high")
#sağ sol kulaklık ayarı?
data[:, 0] = filtfilt(b, a, data[:, 0])
data[:, 1] = filtfilt(b, a, data[:, 1])


wavfile.write("yeni_erkek.wav", samplerate, data) # kaydet


""""
#keyfe göre yap 

# Ses dosyasını görselleştir  
length = data.shape[0]
time = np.linspace(0., length/samplerate, length)
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
"""


