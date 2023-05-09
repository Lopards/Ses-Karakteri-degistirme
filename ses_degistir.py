import scipy.io.wavfile as wav
import numpy as np
import scipy.signal
import tkinter as tk
import matplotlib.pyplot as plt 
import sounddevice as sd
import soundfile as sf
import numpy as np 
import sys

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.ttk import Combobox
from tkinter.messagebox import showinfo
from tkinter import messagebox



def dosya_sec():
    dosya_yolu = fd.askopenfilename(initialdir="/", title="Dosya Seç",
                                    filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    dosya_yolu_kiti.config(text="Dosya YOLU = " + dosya_yolu)


class Ses_Degistir:
    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu
        self.samplerate = None
        self.data = None
        self.nyquist_freq = None
        self.order = None

    def pitch_shift(self, pitch):

        if pitch == 1:
            # dosya yolu verilen ses dosyası oku
            self.samplerate, self.data = wav.read(self.dosya_yolu)
            self.nyquist_freq = 5 * self.samplerate  # Nyquist frekansı hesapla
            self.order = 5
            cutoff_freq = 600.0

            # Kesme frekansı nyquist frekansa bölünerek kesme frekansı hesaplan
            cutoff = cutoff_freq / self.nyquist_freq
            b, a = scipy.signal.butter(
                self.order, cutoff, btype="high")  # butterworth filtresi
            filtreli_data = scipy.signal.filtfilt(
                b, a, self.data)  # filtreli ses dosyasını elde et
            return filtreli_data


# Eğer 2 (kadin) secilirse sesi kadın sesine dondurmeye calış ve filtrelenmiş datayı döndür
        elif pitch == 2:  # Kadın sesi
            self.samplerate, self.data = wav.read(self.dosya_yolu)
            self.nyquist_freq = 1.0 * self.samplerate
            self.order = 5
            cutoff_freq = 2500.0

            cutoff = cutoff_freq / self.nyquist_freq
            b, a = scipy.signal.butter(self.order, cutoff, btype="high")
            filtreli_data = scipy.signal.filtfilt(b, a, self.data)
            return filtreli_data

        # cutoff = cutoff_freq / self.nyquist_freq
        # b, a = scipy.signal.butter(self.order, cutoff, btype="high")
        # filtreli_data = scipy.signal.filtfilt(b, a, self.data)

    def save_wav(self, dosya_yolu1, data):
        wav.write(dosya_yolu1, self.samplerate, np.int16(data))
        

class SoundRecorder:
    def __init__(self):
        self.frames = []
        self.samplerate = 44100
        self.channels = 2
        self.filename = "recordin1g.wav"
        
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
        






master = Tk()
master.title("Ses degistirme Programı")
Canvas = Canvas(master, height=450, width=750)
Canvas.pack()

# pack
# place
# grid

frame_ust = Frame(master, bg='#bdb8c6')  # renk
# gri bölgenin yerini konumladım
frame_ust.place(relx=0.1, rely=0.1, relwidth=0.75, relheight=0.1)

frame_alt_sol = Frame(master, bg='#add8e6')  # renk
frame_alt_sol.place(relx=0.1, rely=0.21, relwidth=0.23, relheight=0.66)

frame_alt_sag = Frame(master, bg='#add8e6')  # renk
frame_alt_sag.place(relx=0.34, rely=0.21, relwidth=0.51, relheight=0.66)


dosya_yolu_kiti = Label(frame_ust, bg='#bdb8c6',
                        text="Dosya YOLU = ", font="Verdana 10 bold")

dosya_yolu_kiti.pack(padx=10, side=LEFT)


#dosya_yolu_opsiyon = StringVar(frame_ust)
# dosya_yolu_opsiyon.set("\t")


#dosya_yolu_acilir_menu.pack(padx=10, side=LEFT)


dosya_sec_button = Button(frame_ust, text="Dosya Seç", command=dosya_sec)
dosya_sec_button.pack(padx=10, side=LEFT)



# PART2##


# sabit olan şeyleri değişkene tanımlayıp hafızada yer kaplamaya gerek yok


Label(frame_alt_sol, text="Hangi sesi istiyorsunuz?", bg='#add8e6',
      font="Verdan 9 bold").pack(padx=10, pady=10, anchor=NW)

var = IntVar()

S1 = Radiobutton(frame_alt_sol, text="Çocuk sesi", variable=var,
                 value=1, bg='#add8e6', font="Verdan 8")
S1.pack(padx=15, pady=5, anchor=NW)

S2 = Radiobutton(frame_alt_sol, text="Kadın sesi", variable=var,
                 value=2, bg='#add8e6', font="Verdan 8")
S2.pack(padx=15, pady=5, anchor=NW)




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








seskayitDurdur_button=Button(frame_ust, text="Kayıt başlat- Durdur",command=SoundRecorderGUI)
seskayitDurdur_button.pack(padx=15,anchor=NW)



## part3###

def calistir():
    dosya_yolu = dosya_yolu_kiti.cget("text").replace("Dosya YOLU = ", "")
    secim = var.get()
    sonMesaj = ""

    if dosya_yolu == "":
        showinfo("Hata", "Lutfen Dosya seçiniz.")

    else:
        if secim == 1:
            sonMesaj += "çocuk sesi sisteme kaydedildi."
            showinfo("başarılı islem", sonMesaj)  # başlık,mesaj

        elif secim == 2:
            sonMesaj += "kadın sesi sisteme kaydedildi."
            showinfo("başarılı islem", sonMesaj)

        else:
            showinfo("Hata", "Lutfen bir secim yapiniz")

    ses_degistirici = Ses_Degistir(dosya_yolu)

    filtreli_data = ses_degistirici.pitch_shift(secim)

    if filtreli_data is not None:
        yeni_dosya = 'yeni_ses.wav'
        ses_degistirici.save_wav(yeni_dosya, filtreli_data)

  
# eğer calistir butonuna basıınca ekranın gitmesini istiyorsan command=master.destroy yap
calistir_button = Button(frame_alt_sol, text="Çalıstır", command=calistir)
calistir_button.pack(anchor=S)

Label(frame_alt_sag, text="Ses diagramı",
      bg='#add8e6', font="Verdan 12 bold").pack()


metin_alani = Text(frame_alt_sag, height=9, width=45)
metin_alani.tag_configure('stil', foreground="#bfbfbf",
                          font=('Verdana', 7, 'bold'))
metin_alani.pack()

master.mainloop()  # mainloop sayesinde arayüz devamlı ekranda kalıyor
