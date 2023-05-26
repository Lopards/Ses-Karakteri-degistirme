
import tkinter as tk
import threading
import pyaudio
import numpy as np
from scipy import signal
import soundfile as sf
import librosa
class SesDegisim:
    def __init__(self):
        self.root = tk.Tk()
        self.basla_button = tk.Button(self.root, text="Başla", command=self.ses_degisimi_baslat)
        self.basla_button.pack()
        self.durdur_button = tk.Button(self.root, text="Durdur", command=self.ses_degisimi_durdur)
        self.durdur_button.pack()

        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.PITCH_SHIFT_FACTOR = 1.1  # erkğe en yakın

        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_running = False
        self.thread = None

    def ses_degisimi_baslat(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.baslat_ses_degisimi)
            self.thread.start()

    def ses_degisimi_durdur(self):
        self.is_running = False
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
        for a in range(int(self.RATE / self.CHUNK * 5)):
            input_data = self.stream.read(self.CHUNK)
            kaydedilen_list.append(input_data)
        
        kaydedilen_sinyal = np.frombuffer(b''.join(kaydedilen_list),dtype=np.float32)
        cinsiyet = self.classify_gender(kaydedilen_sinyal)
        
        if cinsiyet =="Erkek":
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self.hata_mesaji()
        
        else: 
            self.stream.start_stream()
            while self.is_running:
                input_data = self.stream.read(self.CHUNK)
                audio_data = np.frombuffer(input_data, dtype=np.float32) * 0.4

                shifted_audio_data = signal.resample(audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR))

                self.stream.write(shifted_audio_data.tobytes())
                
    def durdur(self):
        self.is_running = False
        self.thread.join()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
    
    def classify_gender(self, audio_data):
        sf.write("temp.wav", audio_data, self.RATE)
        signal, _ = librosa.load("temp.wav", sr=self.RATE)
        if np.mean(signal[0]) > np.mean(signal[1]):
            gender = "Kadın"
        else:
            gender = "Erkek"
        return gender
    
    def hata_mesaji(self):
        error_label = tk.Label(self.root, text="HATA: Mikrofona gelen ses kadın sesidir!")
        error_label.pack()


    def run(self):
        self.root.mainloop()
