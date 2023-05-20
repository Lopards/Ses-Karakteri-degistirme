from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter.messagebox import showinfo
from datetime import datetime
from gtts import gTTS
from tkinter import filedialog as fd

import soundfile as sf
import librosa
import tkinter as tk
import os
import librosa
import numpy as np

import Ses_kaydedici
import Women
import Men_voice
import children_voice

def select_audio_file():
    global filename
    filename = fd.askopenfilename(initialdir="/", title="Dosya Seç",
                                    filetypes=(("Wav files", "*.wav*"), ("all files", "*.*")))
    dosya_yolu_kiti.config(text="Dosya YOLU = " + filename)
    
    

"""""
def run_function(file_path):
    # Seçilen dosya yoluyla bir işlevi çalıştırın
   run= classify(file_path)
   run
 """  
   

def classify(filename):
    
    signal, rate = librosa.load(filename, sr=None, mono=False)
    # Ses sinyalini analiz etmek ve sonucu etiketlemek için gereken işlemler burada yapılacak.

    if np.mean(signal[0]) > np.mean(signal[1]):
        gender = "Kadın"
    else:
        gender = "Erkek"

    return gender



def on_select():
    # Seçili radyo düğmesi değerini alın
    filename = dosya_yolu_kiti.cget("text").replace("Dosya YOLU = ", "")
    selected_option = option.get()
    sonmesaj=""
    
    if filename =="":
        showinfo("hata","Dosya seciniz")
    else:
        if selected_option==1:
            try:
                gender=classify(filename)
                if gender=="Erkek":
                    showinfo("Hata","Zaten ekrek sesi")
                else:
                    Men_voice.men(filename)
                    sonmesaj+="Başarılı şekilde erkek sesi oluştu"
                    showinfo("Başarılı",sonmesaj)
            except:
                    showinfo("hata","beklenmedik bir hata oldu...")   
        
        elif  selected_option == 2:
            try:
                gender=classify(filename)
                if gender=="Kadın":
                    showinfo("Hata","Zaten kadın sesi")
                else:
                    Women.women(filename)
                    sonmesaj+="Başarılı şekilde kadın sesi oluştu"
                    showinfo("Başarılı",sonmesaj)
            except:
                    showinfo("hata","beklenmedik bir hata oldu...") 
        
        elif selected_option == 3:
            try:
                children_voice.children(filename)
                sonmesaj += "Çouck sesine dönüştürüldü."
                showinfo("başarılı işlem", sonmesaj)
            except:
                showinfo("hata", "bir hata oluştu")
        
        else:
            showinfo("Hata", "Lutfen bir secim yapiniz")
            
            
            
            
def metni_kaydet():
    metin = text_alani.get("1.0", "end-1c")
    tarih = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dosya_adi = f"metin_{tarih}.txt"
    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        dosya.write(metin)


                                 
def metni_oku():
    metin = text_alani.get("1.0", "end-1c")
    ses = gTTS(text=metin, lang="tr")
    ses.save("Metin_ses.wav")
    os.system("start Metin_ses.wav")              
            
            
            
        
         

# Ana pencereyi oluştur
root = Tk()
root.title("Ses Dosyası Seçimi")
Canvas = Canvas(root, height=450,width=750)
Canvas.pack()


frame_ustbolge = Frame(root, bg="#0080FF")
frame_ustbolge.place(relx=0.1, rely=0.1, relwidth=0.75, relheight=0.1)

frame_altSol = Frame(root, bg="#0080FF")
frame_altSol.place(relx=0.1, rely=0.21, relwidth=0.36, relheight=0.66)

frame_altSag = Frame(root, bg="#0080FF")
frame_altSag.place(relx=0.47, rely=0.21, relwidth=0.38, relheight=0.66)


# frame_altsag içerisine metin giriş alanı (text_alanı) ekleme
text_alani = tk.Text(frame_altSag, height=6, width=40)
text_alani.pack(side="top", padx=5, pady=5)




# Metni kaydetme butonu (kaydet_butonu)
kaydet_butonu = tk.Button(
    frame_altSag, text="Metni Kaydet", command=metni_kaydet)
kaydet_butonu.pack(side="top", padx=5, pady=5)

# Metni okuma butonu (okuma_butonu)
okuma_butonu = tk.Button(frame_altSag, text="Metni Oku", command=metni_oku)
okuma_butonu.pack(side="top", padx=5, pady=5)


dosya_yolu_kiti = Label(frame_ustbolge, bg='#0080FF',
                        text="Dosya YOLU = ", font="Verdana 10 bold")
dosya_yolu_kiti.pack(padx=10, side=LEFT)


seskayitDurdur_button = Button(
    frame_ustbolge, text="Kayıt başlat- Durdur", command=Ses_kaydedici.SesKaydedici)
seskayitDurdur_button.pack(padx=15, pady=10, side=RIGHT)



# Dosya seçme düğmesini 
select_button = Button(frame_ustbolge, text="Dosya Seç", command=select_audio_file)
select_button.pack(padx=10,side=LEFT)

# Uyarı mesajını gösterecek etiket
warning_label = Label(root, text="")
warning_label.pack()

# Radyo düğmelerini oluştur
option = IntVar()

male_radio = Radiobutton(frame_altSol, text="Erkek sesi", variable=option,
                 value=1, bg='#add8e6', font="Verdan 8")
male_radio.pack(padx=15, pady=5, anchor=NW)

female_radio = Radiobutton(frame_altSol, text="Kadın sesi", variable=option,
                 value=2, bg='#add8e6', font="Verdan 8")
female_radio.pack(padx=15, pady=5, anchor=NW)

child_radio = Radiobutton(frame_altSol, text="Çocuk sesi", variable=option,
                 value=3, bg='#add8e6', font="Verdan 8")
child_radio.pack(padx=15, pady=5, anchor=NW)

# Çalıştır düğmesini oluştur
run_button = Button(frame_altSol, text="Çalıstır", command=on_select)
run_button.pack(anchor=S)

# Ana döngüyü başlat
root.mainloop()
