from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from gtts import gTTS
from playsound import playsound

 
import tkinter as tk
from gtts import gTTS
from playsound import playsound



def metin():
    def kaydet_oku():
        text = text_entry.get("1.0", tk.END).strip()  # metni al
        if text:
            # metni wav dosyasına dönüştür
            language = 'tr'  
            speech = gTTS(text=text, lang=language, slow=False)
            speech.save("output.wav")
            # mp3 dosyasını oynat
            playsound("output.wav")

    # tkinter penceresi oluştur
    window = tk.Tk()
    window.title("Metin Okuma")

    # metin giriş kutusu
    text_entry = tk.Text(window, height=10, width=50)
    text_entry.pack()

    # kaydet ve oku düğmeleri
    save_button = tk.Button(window, text="Kaydet ve Oku", command=kaydet_oku)
    save_button.pack()

    # pencereyi göster
    window.mainloop()
