import tkinter as tk
import threading
import pyaudio
import numpy as np
from scipy import signal

class SesDegisim:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.PITCH_SHIFT_FACTOR = 1.1

        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_running = False

    def baslat(self):
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.CHUNK)
        self.is_running = True

        while self.is_running:
            input_data = self.stream.read(self.CHUNK)
            audio_data = np.frombuffer(input_data, dtype=np.float32)*0.4
            
            shifted_audio_data = signal.resample(audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR))
            
            self.stream.write(shifted_audio_data.tobytes())

    def durdur(self):
        if self.is_running:
            self.is_running = False
            self.stream.stop_stream()
            self.stream.close()

            self.p.terminate()

class Uygulama:
    def __init__(self, root):
        self.root = root
        self.ses_donusumu = SesDegisim()
        self.basla_button = tk.Button(root, text="Başla", command=self.baslat)
        self.durdur_button = tk.Button(root, text="Durdur", command=self.durdur)
        self.basla_button.pack()
        self.durdur_button.pack()

    def baslat(self):
        self.thread = threading.Thread(target=self.ses_donusumu.baslat)
        self.thread.start()
        self.root.mainloop()

    def durdur(self):
        self.ses_donusumu.durdur()
        self.thread.join()
        
    def run(self):
        root = tk.Tk()
        uygulama = Uygulama(root)
        root.mainloop()


