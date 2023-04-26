import scipy.io.wavfile as wav
import numpy as np
import scipy.signal


class Ses_Degistir:
    def __init__(self, dosya_yolu):
     self.dosya_yolu = dosya_yolu  
     
    def pitch_shift(self, pitch):
        if pitch == 1:  # Erkek sesi
            self.samplerate, self.data = wav.read(dosya_yolu) #dosya yolu verilen ses dosyası oku
            self.nyquist_freq = 0.2 * self.samplerate #Nyquist frekansı hesapla
            self.order = 9
            cutoff_freq = 600.0

            cutoff = cutoff_freq / self.nyquist_freq #Kesme frekansı nyquist frekansa bölünerek kesme frekansı hesaplan
            b, a = scipy.signal.butter(self.order, cutoff, btype="low") #butterworth filtresi
            filtreli_data = scipy.signal.filtfilt(b, a, self.data) # filtreli ses dosyasını elde et
            return filtreli_data

        elif pitch == 2:  # Kadın sesi
            self.samplerate, self.data = wav.read(dosya_yolu)
            self.nyquist_freq = 1.0 * self.samplerate
            self.order = 5
            cutoff_freq = 2500.0

            cutoff = cutoff_freq / self.nyquist_freq
            b, a = scipy.signal.butter(self.order, cutoff, btype="high")
            filtreli_data = scipy.signal.filtfilt(b, a, self.data)
            return filtreli_data
        else:
            print("Hatali giriş! Lütfen 1 veya 2 tuşlarina basın.")
            return 

        #cutoff = cutoff_freq / self.nyquist_freq
        #b, a = scipy.signal.butter(self.order, cutoff, btype="high")
        #filtreli_data = scipy.signal.filtfilt(b, a, self.data)

    def save_wav(self, dosya_yolu, data):
        wav.write(dosya_yolu, self.samplerate, np.int16(data))


if __name__ == '__main__':
    dosya_yolu = 'C:/rise_teknoloji/deneme.wav'
    ses_degistirici = Ses_Degistir(dosya_yolu)
    print("Sesi değiştirmek için 1'e basın (erkek sesi), 2'ye basın (kadın sesi):")
    choice = int(input())
    filtreli_data = ses_degistirici.pitch_shift(choice)
    if filtreli_data is not None:
        yeni_dosya = 'new21_ses.wav'
        ses_degistirici.save_wav(yeni_dosya, filtreli_data)
        print("{} dosyasi başariyla {} dosyasina dönüştürüldü. :D".format(dosya_yolu, yeni_dosya))
        
    else:
        print("dosya donusturulurken bir sorun ollustu :(")
