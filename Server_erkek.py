import numpy as np
import pyaudio

def make_old_man_voice():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Ses dosyasının tonunu değiştir.
    def change_pitch(audio, n_semitones):
        # Ses dosyasını frekans alanına dönüştür.
        frequencies = np.fft.fft(audio)

        # Frekansları belirtilen yarıton kadar kaydır.
        frequencies = frequencies * np.exp(2 * np.pi * n_semitones / 12)

        # Frekansları zaman alanına geri dönüştür.
        audio = np.fft.ifft(frequencies)

        # Tonu değiştirilmiş ses dosyasını döndür.
        return audio

    # Ses dosyasının hızını değiştir.
    def change_speed(audio, rate):
        """
        Sesin hızını belirtilen oranda değiştirir.
    
        Args:
            audio: Hızı değiştirilecek ses.
            rate: Hız değişikliği oranı.
    
        Returns:
            Hızı değiştirilmiş ses.
        """
        # Yeni hızda sesi çalmak için bir örnekleyici oluştur.
        output = pyaudio.PyAudio()

        # Çıkış için yeni bir stream oluştur.
        output_stream = output.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=int(RATE * rate),
                                    output=True)

        # Sesin hızını değiştirerek çal.
        output_stream.write(audio.astype(np.int16).tobytes())

        # Streami kapat.
        output_stream.stop_stream()
        output_stream.close()
        output.terminate()

    # Mikrofondan gelen sesi al ve işle.
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Tonu değiştir.
        audio_data = change_pitch(audio_data, -11)

        # Hızı değiştir.
        change_speed(audio_data, 1.3)

    # Streami kapat.
    stream.stop_stream()
    stream.close()
    p.terminate()
 