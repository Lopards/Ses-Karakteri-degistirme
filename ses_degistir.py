import matplotlib.pyplot as plt #görselleştirme için
from scipy.io import wavfile 
from scipy.signal import resample, butter, filtfilt # resample, butter, filtfilt fonksiyonları yüklenir
import numpy as np 

samplerate, data = wavfile.read("C:/rise_teknoloji/deneme.wav") 



# ses sinayline ayar vererek tonu değiştir

nyquist_freq = 6.0 * samplerate # Nyquist frekansı hesaplanır
cutoff_freq = 600.0 # Hz
order = 6 # filtrenin mertebesini belirle
cutoff = cutoff_freq / nyquist_freq # kesme frekansı hesaplanır
b, a = butter(order, cutoff, btype="high") #filtre tasarla

data = data.reshape((-1, 2)) #data 1 boyutlu ise 2 ye çıkartıyoruz 

data[:, 0] = filtfilt(b, a, data[:, 0]) # sol kanalın verisi filtreden geçir
data[:, 0] = filtfilt(b, a, data[:, 0]) # sağ kanalın verisi 

wavfile.write("yeni2_ses.wav", samplerate, data) #   yeni bir dosya oluştur



# Ses dosyasını görselleştirme
length = data.shape[0] # verinin boyutu alınır
time = np.linspace(0., length/samplerate, length) # zaman dizisi oluşturulur
plt.plot(time, data[:, 0], label="Left channel") # sol kanalın verisi çizilir
plt.plot(time, data[:, 1], label="Right channel") # sağ kanalın verisi çizilir
plt.legend() # etiketleri ekle
plt.xlabel("Time [s]") # x ekseni 
plt.ylabel("Amplitude") # y ekseni etiketi
plt.show() # çizimi göster
