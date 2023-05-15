import tkinter as tk
import librosa
from tkinter import filedialog as fd
import numpy as np

class classify_voice:
    def __init__(self, result_label):
        self.result_label = result_label

    def classify(self, filename):
        signal, rate = librosa.load(filename, sr=None, mono=False)

        # Ses sinyalini analiz etmek ve sonucu etiketlemek için gereken işlemler burada yapılacak.

        
        if np.mean(signal[0]) > np.mean(signal[1]):
            gender = "Kadın"
        else:
            gender = "Erkek"

        # Sonucu bir etiketle göster
        self.result_label.configure(text=f"Ses {gender} sesine benziyor.")



class SesSiniflandirmaProgrami:
    def __init__(self):
        # Tkinter penceresi oluşturma
        self.window = tk.Tk()
        self.window.title("Ses Sınıflandırma Programı")

        # Ses dosyası 
        file_label = tk.Label(self.window, text="Ses dosyası: ")
        file_label.pack(side=tk.LEFT)
        self.file_entry = tk.Entry(self.window)
        self.file_entry.pack(side=tk.LEFT)
        browse_button = tk.Button(self.window, text="Dosya Seç", command=self.dosya_ara)
        browse_button.pack(side=tk.LEFT)

        # Sınıflandırma 
        classify_button = tk.Button(self.window, text="Sınıflandır", command=self.classify)
        classify_button.pack(side=tk.LEFT)
        
        
        # Sonuç etiketi
        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()
        self.voice_classifier = classify_voice(self.result_label) 
        
        self.filename = ""  # Dosya adı için boş bir özellik oluşturun
        
        # Pencereyi çalıştırma
        self.window.mainloop()
   
    def dosya_ara(self):
        self.filename = fd.askopenfilename()  # Dosya adını self.filename'e ata
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(tk.END, self.filename)
 
    def classify(self):
        if self.filename:
            self.voice_classifier.classify(self.filename)  # Dosya adını sınıflandırma sınıfına geçirin
        else:
            self.result_label.configure(text="Lütfen ses dosyası seçin.")

