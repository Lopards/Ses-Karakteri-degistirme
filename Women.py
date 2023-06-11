import numpy as np
from scipy.io import wavfile

def make_lady_voice(audio_file):

    #Bir .wav ses dosyasını yaşlı kadın sesine dönüştürür.

    # Ses dosyasını yükle.
    sample_rate, audio = wavfile.read(audio_file)

    # Ses dosyasının tonunu değiştir.
    audio = change_pitch(audio, -27)*1.2 # ses yüksek çıkması için 1.2

    # Ses dosyasının hızını değiştir.
    audio = change_speed(audio, 0.85)
    
    

    # Veri türünü uygun şekilde dönüştür.
    audio = audio.astype(np.float32)

    # Dönüştürülmüş ses dosyasını kaydet.
    
    wavfile.write("old_women_voice.wav", sample_rate, audio)

def change_pitch(audio, n_semitones):
    """
    Ses dosyasının tonunu belirtilen yarıton kadar değiştirir.

    Args:
        audio: Tonu değiştirilecek ses dosyası.
        n_semitones: Ton değişikliği miktarı (yarıton cinsinden).
        """


    # Ses dosyasını frekans alanına dönüştür.
    frequencies = np.fft.fft(audio)

    # Frekansları belirtilen yarıton kadar kaydır.
    frequencies = frequencies * np.exp( 0.9 * (np.pi+1) * (n_semitones) / 10)

    # Frekansları zaman alanına geri dönüştür.
    audio = np.fft.ifft(frequencies)

    # Tonu değiştirilmiş ses dosyasını döndür.
    return audio

def change_speed(audio, rate):
    """
    Ses dosyasının hızını belirtilen oranda değiştirir.

    Args:
        audio: Hızı değiştirilecek ses dosyası.
        rate: Hız değişikliği oranı.

    Returns:
        Hızı değiştirilmiş ses dosyası.
    """

    # Ses dosyasını zaman alanına dönüştür.
    samples = np.arange(audio.size)

    # Yeni örnek noktalarını hesapla.
    new_samples = np.linspace(0, samples[-1], int(samples[-1] * (rate)) + 1)

    # Yeni örnek noktalarını tam sayıya dönüştür.
    new_samples = new_samples.astype(int)

    # Yeni örnek noktalarını kullanarak ses dosyasını yeniden örnekle.
    new_audio = audio[new_samples]

    # Hızı değiştirilmiş ses dosyasını döndür.
    return new_audio
