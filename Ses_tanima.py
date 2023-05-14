import tkinter as tk
import librosa
import numpy as np
from tkinter import filedialog as fd
def Ses():
 def classify_voice():
    filename = "kayit.wav"  # kaydedilen ses dosyasının adı
    signal, rate = librosa.load(filename, sr=None, mono=False)

    # Ses sinyalini analiz etmek ve sonucu etiketlemek için gereken işlemler burada yapılacak.

    # Örnek olarak, sadece kadın ve erkek sınıfları varsa, örnek bir karar aşaması yazalım:
    if np.mean(signal[0]) > np.mean(signal[1]):
        gender = "Kadın"
    else:
        gender = "Erkek"

    # Sonucu bir etiketle göster
    result_label.configure(text=f"Ses {gender} sesine benziyor.")

    # Tkinter penceresi oluşturma
    window = tk.Tk()
    window.title("Ses Sınıflandırma Programı")

    # Dosya seçme butonu oluşturma
    file_label = tk.Label(window, text="Ses dosyası: ")
    file_label.pack(side=tk.LEFT)
    file_entry = tk.Entry(window)
    file_entry.pack(side=tk.LEFT)
    browse_button = tk.Button(window, text="Dosya Seç", command=fd.askopenfilename(initialdir="/", title="Dosya Seç",
                                        filetypes=(("Text files", "*.txt*"), ("all files", "*.*"))))
    browse_button.pack(side=tk.LEFT)

    # Sınıflandırma butonu oluşturma
    classify_button = tk.Button(window, text="Sınıflandır", command=classify_voice)
    classify_button.pack(side=tk.LEFT)

    # Sonuç etiketi oluşturma
    result_label = tk.Label(window, text="")
    result_label.pack()

    # Pencereyi çalıştırma
    window.mainloop()


