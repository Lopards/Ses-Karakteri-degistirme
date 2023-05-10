import tkinter as tk
import sounddevice as sd
import soundfile as sf
import numpy as np
import sys

class SoundRecorder:
    def __init__(self):
        self.frames = []
        self.samplerate = 44100
        self.channels = 2
        self.filename = "kayit.wav"
        
    def start_recording(self):
        self.frames = []
        sd.default.samplerate = self.samplerate
        sd.default.channels = self.channels
        sd.default.dtype = "float32"
        sd.InputStream(callback=self.callback).start()
        
    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.frames.append(indata.copy())
        
    def stop_recording(self):
        sd.stop()
        self.save_file()
        
    def save_file(self):
        data = np.concatenate(self.frames, axis=0)
        sf.write(self.filename, data, self.samplerate)
        

class SoundRecorderGUI:
    def __init__(self):
        self.recorder = SoundRecorder()
        
        self.root = tk.Tk()
        self.root.title("Ses Kayıt Arayüzü")
        
        self.record_button = tk.Button(self.root, text="Ses Kaydı Başlat", command=self.start_recording)
        self.record_button.pack()
        
        self.stop_button = tk.Button(self.root, text="Ses Kaydını Durdur", command=self.stop_recording, state="disabled")
        self.stop_button.pack()
        
        self.root.mainloop()
        
    def start_recording(self):
        self.recorder.start_recording()
        self.record_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
    def stop_recording(self):
        self.recorder.stop_recording()
        self.record_button.config(state="normal")
        self.stop_button.config(state="disabled")

       


