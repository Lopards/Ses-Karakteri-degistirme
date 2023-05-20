import tkinter as tk
import pyaudio
import numpy as np
import soundfile as sf

class SesKaydedici:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ses Kaydı ve Cinsiyet Ayrımı")
        self.baslat_buton = tk.Button(self.root, text="Kayıt Al", command=self.kaydi_baslat)
        self.baslat_buton.pack(side=tk.LEFT)
        
        self.durdur_button = tk.Button(self.root, text="Kaydı Durdur", command=self.kaydi_durdur)
        self.durdur_button.pack(side=tk.LEFT)
        
        self.p = pyaudio.PyAudio()
        self.sample_rate = 44100
        self.recording = False
        self.frames = []
        self.input_device_info = self.p.get_default_input_device_info()
        self.channels = self.input_device_info['maxInputChannels']
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  input=True,
                                  input_device_index=None,
                                  stream_callback=self.audio_callback)
        
    def kaydi_baslat(self):
        self.recording = True
        self.frames = []
        self.stream.start_stream()
    
    def kaydi_durdur(self):
        
        self.recording = False
        self.stream.stop_stream()
        signal = np.concatenate(self.frames)
        gender = self.classify(signal)
        result_label = tk.Label(self.root, text=f"Kaydedilen sesin cinsiyeti: {gender}")
        result_label.pack()
        
        output_file = f"kaydedilen_{gender}_ses.wav"
        sf.write(output_file, signal, self.sample_rate)
        
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.recording:
            signal = np.frombuffer(in_data, dtype=np.float32).reshape(-1, self.channels)
            self.frames.append(signal)
        return (in_data, pyaudio.paContinue)
    
    def classify(self, signal):
        if np.mean(signal[0]) > np.mean(signal[1]):
            gender = "Kadın"
        else:
            gender = "Erkek"
        return gender
    
    def run(self):
        self.root.mainloop()



