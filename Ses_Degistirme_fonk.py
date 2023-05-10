import scipy.io.wavfile as wav
import numpy as np
import scipy.signal
import numpy as np 


class Ses_Degistir:
    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu
        self.samplerate = None
        self.data = None
        self.nyquist_freq = None
        self.order = None
        

    def pitch_shift(self, pitch):

        if pitch == 1:
            # dosya yolu verilen ses dosyası oku
          
            self.samplerate, self.data = wav.read(self.dosya_yolu)
            
            self.nyquist_freq = 5 * self.samplerate  # Nyquist frekansı hesapla
            self.order = 5
            cutoff_freq = 600.0

            # Kesme frekansı nyquist frekansa bölünerek kesme frekansı hesaplan
            cutoff = cutoff_freq / self.nyquist_freq
            b, a = scipy.signal.butter(
                self.order, cutoff, btype="high")  # butterworth filtresi
            filtreli_data = scipy.signal.filtfilt(
                b, a, self.data)  # filtreli ses dosyasını elde et
           
            return filtreli_data


# Eğer 2 (kadin) secilirse sesi kadın sesine dondurmeye calış ve filtrelenmiş datayı döndür
        elif pitch == 2:  # Kadın sesi
            self.samplerate, self.data = wav.read(self.dosya_yolu)
            self.nyquist_freq = 1.0 * self.samplerate
            self.order = 5
            cutoff_freq = 2500.0

            cutoff = cutoff_freq / self.nyquist_freq
            b, a = scipy.signal.butter(self.order, cutoff, btype="high")
            filtreli_data = scipy.signal.filtfilt(b, a, self.data)
            filtreli_data = scipy.signal.filtfilt(b, a, self.data, padlen=50)
            
            return filtreli_data

        # cutoff = cutoff_freq / self.nyquist_freq
        # b, a = scipy.signal.butter(self.order, cutoff, btype="high")
        # filtreli_data = scipy.signal.filtfilt(b, a, self.data)
       

    def save_wav(self, dosya_yolu1, data):
        wav.write(dosya_yolu1, self.samplerate, np.int16(data))
