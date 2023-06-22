import tkinter as tk
import threading
import pyaudio
import numpy as np
from scipy import signal
import soundfile as sf
import time

class SesDegisim:
    def __init__(self):
        self.root = tk.Tk()
        self.basla_button = tk.Button(self.root, text="Başlat", command=self.ses_degisimi_baslat)
        self.basla_button.pack()
        self.durdur_button = tk.Button(self.root, text="Durdur", command=self.ses_degisimi_durdur)
        self.durdur_button.pack()
        self.bas_konus_button = tk.Button(self.root, text="BAS-KONUS", command=self.bas_konus)
        self.bas_konus_button.pack()

        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.PITCH_SHIFT_FACTOR = 0.85
        self.DELAY_SECONDS = 0 # Değişiklik: Delay süresi 0 saniye olarak ayarlandı

        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_running = False
        self.is_paused = False
        self.is_gender_change_paused = False
        self.thread = None

        self.root.bind('<Key>', self.klavye_kontrol)

    def klavye_kontrol(self, event):
        if event.char == 'q':
            if self.is_running and not self.is_paused:
                self.is_paused = True
            elif self.is_running and self.is_paused:
                self.is_paused = False
                self.bas_konus()

    def bas_konus(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.baslat_ses_degisimi)
            self.thread.start()

    def ses_degisimi_baslat(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.baslat_ses_degisimi)
            self.thread.start()

    def ses_degisimi_durdur(self):
        self.is_running = False
        self.is_gender_change_paused = False
        self.thread.join()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

    def baslat_ses_degisimi(self):
        self.is_running = True
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.CHUNK)

        kaydedilen_list = []
        while self.is_running:
            input_data = self.stream.read(self.CHUNK)
            kaydedilen_list.append(input_data)
            audio_data = np.frombuffer(input_data, dtype=np.float32) * 0.5

            if len(kaydedilen_list) > int(self.RATE / self.CHUNK * self.DELAY_SECONDS):
                kaydedilen_sinyal = np.frombuffer(b''.join(kaydedilen_list[-int(self.RATE / self.CHUNK * self.DELAY_SECONDS):]), dtype=np.int16)
                cinsiyet = self.classify_gender(kaydedilen_sinyal)

                if cinsiyet == "Erkek":
                    shifted_audio_data = signal.resample(audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR))
                    self.stream.write(shifted_audio_data.tobytes())
                elif cinsiyet == "Kadın":
                    # Ses değiştirme fonksiyonuna girmeden doğrudan sesi yolla
                    self.stream.write(audio_data.tobytes())

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def classify_gender(self, audio_data):
        if np.mean(audio_data) > 0:
            gender = "Kadın"
        else:
            gender = "Erkek"
        return gender

    def hata_mesaji(self):
        error_label = tk.Label(self.root, text="HATA: Zaten Kadın sesi!")
        error_label.pack()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ses_degisim = SesDegisim()
    ses_degisim.run()
