from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from datetime import datetime
from gtts import gTTS

import librosa
import tkinter as tk
import os
import librosa
import numpy as np

import Ses_tanima
import Ses_kaydedici
import Women
import Men_voice
import children_voice


def dosya_sec():
    dosya_yolu = fd.askopenfilename(initialdir="/", title="Dosya Seç",
                                    filetypes=(("Wav files", "*.wav*"), ("all files", "*.*")))
    dosya_yolu_kiti.config(text="Dosya YOLU = " + dosya_yolu)


arayuz = Tk()
arayuz.title = "Ses Degistime programi"
Canvas = Canvas(arayuz, height=450, width=750)
Canvas.pack()

frame_ustbolge = Frame(arayuz, bg="#0080FF")
frame_ustbolge.place(relx=0.1, rely=0.1, relwidth=0.75, relheight=0.1)

frame_altSol = Frame(arayuz, bg="#0080FF")
frame_altSol.place(relx=0.1, rely=0.21, relwidth=0.36, relheight=0.66)

frame_altSag = Frame(arayuz, bg="#0080FF")
frame_altSag.place(relx=0.47, rely=0.21, relwidth=0.38, relheight=0.66)


# frame_altsag içerisine metin giriş alanı (text_alanı) ekleme
text_alani = tk.Text(frame_altSag, height=6, width=40)
text_alani.pack(side="top", padx=5, pady=5)

# Metni kaydetme butonu (kaydet_butonu)


def metni_kaydet():
    metin = text_alani.get("1.0", "end-1c")
    tarih = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dosya_adi = f"metin_{tarih}.txt"
    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        dosya.write(metin)


kaydet_butonu = tk.Button(
    frame_altSag, text="Metni Kaydet", command=metni_kaydet)
kaydet_butonu.pack(side="top", padx=5, pady=5)

# Metni okuma butonu (okuma_butonu)


def metni_oku():
    metin = text_alani.get("1.0", "end-1c")
    ses = gTTS(text=metin, lang="tr")
    ses.save("Metin_ses.wav")
    os.system("start Metin_ses.wav")

    


okuma_butonu = tk.Button(frame_altSag, text="Metni Oku", command=metni_oku)
okuma_butonu.pack(side="top", padx=5, pady=5)


dosya_yolu_kiti = Label(frame_ustbolge, bg='#0080FF',
                        text="Dosya YOLU = ", font="Verdana 10 bold")
dosya_yolu_kiti.pack(padx=10, side=LEFT)

dosya_sec_button = Button(frame_ustbolge, text="Dosya Seç", command=dosya_sec)
dosya_sec_button.pack(padx=10, side=LEFT)

#metin_button= Button(frame_altSag,text="metin gir",command=METIN_YERI.metin)
#metin_button.pack(pady=30, side="top")

seskayitDurdur_button = Button(
    frame_ustbolge, text="Kayıt başlat- Durdur", command=Ses_kaydedici.SoundRecorderGUI)
seskayitDurdur_button.pack(padx=15, pady=10, side=RIGHT)


ses_tanimaButton = Button(
    frame_altSag, text="Ses sınıflandırıcı", command=Ses_tanima.SesSiniflandirmaProgrami)
ses_tanimaButton.pack(padx=15, pady=10, side=RIGHT)


Label(frame_altSol, text="Hangi sesi istiyorsunuz?", bg="#0080FF",
      font="Verdan 9 bold").pack(padx=10, pady=10, anchor=NW)

var = IntVar()

S1 = Radiobutton(frame_altSol, text="Erkek sesi", variable=var,
                 value=1, bg='#add8e6', font="Verdan 8")
S1.pack(padx=15, pady=5, anchor=NW)

S2 = Radiobutton(frame_altSol, text="Kadın sesi", variable=var,
                 value=2, bg='#add8e6', font="Verdan 8")
S2.pack(padx=15, pady=5, anchor=NW)

S3 = Radiobutton(frame_altSol, text="Çocuk sesi", variable=var,
                 value=3, bg='#add8e6', font="Verdan 8")
S3.pack(padx=15, pady=5, anchor=NW)


def calistir():
    dosya_yolu = dosya_yolu_kiti.cget("text").replace("Dosya YOLU = ", "")
    secim = var.get()
    sonMesaj = ""
    
    if dosya_yolu == "":
        showinfo("Hata", "Lutfen Dosya seçiniz.")

    else:
        if secim == 1:
            
            try:
                 signal, rate = librosa.load(dosya_yolu, sr=None, mono=False)
                 if np.mean(signal[0]) < np.mean(signal[1]):  
                    sonMesaj+="zaten erkek sesi!"
                    showinfo("Hata", sonMesaj)
                    
                 else:
                    Men_voice.men(dosya_yolu)
                    sonMesaj+="Başarılı bir şekilde erkek sesine donüştürüldü"
                    showinfo("başarılı",sonMesaj)
                    
            except:
                showinfo("h1ata", "bir hata oluştu")

        elif secim == 2:
            try:
                signal, rate = librosa.load(dosya_yolu, sr=None, mono=False)
                if np.mean(signal[0]) > np.mean(signal[1]):  
                    sonMesaj+="zaten kadın sesi"
                    showinfo("Hata", sonMesaj)
                    
                else:
                    Women.women(dosya_yolu)
                    sonMesaj+="Başarılı bir şekilde kadın sesine donüştürüldü"
                    showinfo("başarılı",sonMesaj)
            except:
                showinfo("hata", "bir hata oluştu")

        elif secim == 3:
            try:
                children_voice.children(dosya_yolu)
                sonMesaj += "Çouck sesine dönüştürüldü."
                showinfo("başarılı işlem", sonMesaj)
            except:
                showinfo("hata", "bir hata oluştu")

        else:
            showinfo("Hata", "Lutfen bir secim yapiniz")


calistir_button = Button(frame_altSol, text="Çalıstır", command=calistir)
calistir_button.pack(anchor=S)


arayuz.mainloop()