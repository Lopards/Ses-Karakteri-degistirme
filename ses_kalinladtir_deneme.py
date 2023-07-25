import pyaudio
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

CHUNK = 1024  # Ses veri paketinin boyutu
FORMAT = pyaudio.paInt16  # Ses veri formatı
CHANNELS = 1  # Mono olarak kaydediyoruz
RATE = 44100  # Örnekleme hızı

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

while True:
    data = stream.read(CHUNK)
    # Ses verisini işleme adımlarını buraya ekleyin

    # Ses verisini numpy dizisine dönüştürün
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Ses verisini kalınlaştırma işlemini uygulayın
    amplified_audio_data = audio_data * 2  # Ses verisini 2 katına çıkararak güçlendirin

    # Numpy dizisini pydub AudioSegment objesine dönüştürün
    audio_segment = AudioSegment(
        amplified_audio_data.tobytes(),
        frame_rate=RATE,
        sample_width=p.get_sample_size(FORMAT),
        channels=CHANNELS
    )

    # Kalınlaştırılmış sesi hoparlöre verin
    play(audio_segment)

stream.stop_stream()
stream.close()

p.terminate()
