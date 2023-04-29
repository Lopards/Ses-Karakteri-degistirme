import scipy.io.wavfile as wav
import numpy as np
import scipy.signal
import tkinter as tk


from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.ttk import Combobox
from tkinter.messagebox import showinfo

dosya_yolu = 'C:/rise_teknoloji/deneme.wav'
class Ses_Degistir:
    def __init__(self, dosya_yolu):
     self.dosya_yolu = dosya_yolu

    """
    pitch   : curtain chosn acording to the selection: 1(male), 2(female)
    """

    def pitch_shift(self, pitch):
        
        #Eğer 1 (erkek) secilirse sesi kadın sesine dondurmeye calış ve filtrelenmiş datayı döndür
        if pitch == 1:  # Erkek sesi
            # dosya yolu verilen ses dosyası oku
            self.samplerate, self.data = wav.read(dosya_yolu)
            self.nyquist_freq = 0.2 * self.samplerate  # Nyquist frekansı hesapla
            self.order = 9
            cutoff_freq = 600.0

            # Kesme frekansı nyquist frekansa bölünerek kesme frekansı hesaplan
            cutoff = cutoff_freq / self.nyquist_freq
            b, a = scipy.signal.butter(
                self.order, cutoff, btype="low")  # butterworth filtresi
            filtreli_data = scipy.signal.filtfilt(
                b, a, self.data)  # filtreli ses dosyasını elde et
            return filtreli_data


#Eğer 2 (kadin) secilirse sesi kadın sesine dondurmeye calış ve filtrelenmiş datayı döndür
        elif pitch == 2:  # Kadın sesi
            self.samplerate, self.data = wav.read(dosya_yolu)
            self.nyquist_freq = 1.0 * self.samplerate
            self.order = 5
            cutoff_freq = 2500.0

            cutoff = cutoff_freq / self.nyquist_freq
            b, a = scipy.signal.butter(self.order, cutoff, btype="high")
            filtreli_data = scipy.signal.filtfilt(b, a, self.data)
            return filtreli_data
        else:
            print("Hatali giriş! Lütfen 1 veya 2 tuşlarina basın.")
            return

        # cutoff = cutoff_freq / self.nyquist_freq
        # b, a = scipy.signal.butter(self.order, cutoff, btype="high")
        # filtreli_data = scipy.signal.filtfilt(b, a, self.data)

    def save_wav(self, dosya_yolu1, data):
        wav.write(dosya_yolu1, self.samplerate, np.int16(data))




master = Tk()
Canvas = Canvas(master, height=450, width=750)
Canvas.pack()
master.title("Ses degistirme Programı")
# pack
# place
# grid

frame_ust = Frame(master, bg='#add8e6')  # renk
# mavi bölgenin yerini konumladım
frame_ust.place(relx=0.1, rely=0.1, relwidth=0.75, relheight=0.1)

frame_alt_sol = Frame(master, bg='#add8e6')  # renk
frame_alt_sol.place(relx=0.1, rely=0.21, relwidth=0.23, relheight=0.66)

frame_alt_sag = Frame(master, bg='#add8e6')  # renk
frame_alt_sag.place(relx=0.34, rely=0.21, relwidth=0.51, relheight=0.66)

def dosya_sec():
    dosya_yolu = fd.askopenfilename(initialdir="/", title="Dosya Seç",
                                    filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    dosya_yolu_kiti.config(text="Dosya YOLU = " + dosya_yolu)

dosya_yolu_kiti = Label(frame_ust, bg='#add8e6',
                        text="Dosya YOLU = ", font="Verdana 10 bold")

dosya_yolu_kiti.pack(padx=10, side=LEFT)


dosya_yolu_opsiyon = StringVar(frame_ust)
#dosya_yolu_opsiyon.set("\t")


#dosya_yolu_acilir_menu.pack(padx=10, side=LEFT)


dosya_sec_button = Button(frame_ust, text="Dosya Seç", command=dosya_sec)
dosya_sec_button.pack(padx=10, side=LEFT)


# PART2##


# sabit olan şeyleri değişkene tanımlayıp hafızada yer kaplamaya gerek yok



Label(frame_alt_sol, text="Hangi sesi istiyorsunuz?", bg='#add8e6',
      font="Verdan 8 bold").pack(padx=10, pady=10, anchor=NW)

var = IntVar()

S1 = Radiobutton(frame_alt_sol, text="Çocuk sesi", variable=var,
                 value=1, bg='#add8e6', font="Verdan 7")
S1.pack(padx=15, pady=5, anchor=NW)

S2 = Radiobutton(frame_alt_sol, text="Kadın sesi", variable=var,
                 value=2, bg='#add8e6', font="Verdan 7")
S2.pack(padx=15, pady=5, anchor=NW)

           

#chatgpt

def apply_child_effect(dosya_yolu):
            samplerate, data = wav.read(dosya_yolu)
            nyquist_freq = 0.2 * samplerate  # Nyquist frekansı hesapla
            order = 9
            cutoff_freq = 600.0

            # Kesme frekansı nyquist frekansa bölünerek kesme frekansı hesaplan
            cutoff = cutoff_freq /nyquist_freq
            b, a = scipy.signal.butter(
                order, cutoff, btype="low")  # butterworth filtresi
            filtreli_data = scipy.signal.filtfilt(
                b, a, data)  # filtreli ses dosyasını elde et
            return filtreli_data



## part3###

def calistir():
    
    dosya_yolu = dosya_yolu_kiti.cget("text").replace("Dosya YOLU = ", "")
    secim = var.get()
    
    showinfo(dosya_yolu, secim)
    
    
    ses_degistirici = Ses_Degistir(dosya_yolu)
    

    filtreli_data = ses_degistirici.pitch_shift(secim)
    
    if filtreli_data is not None:
        yeni_dosya = 'yeni_ses.wav'
        ses_degistirici.save_wav(yeni_dosya, filtreli_data)
    
    """
    # Dosya yolu alınır
    dosya_yolu = dosya_yolu_kiti.cget("text").replace("Dosya YOLU = ", "")
    # Hangi sesin seçildiği alınır
    secim = var.get()
    if secim == 1:
       
    # Çocuk sesi seçildi
        data = apply_child_effect(dosya_yolu)
        wavfile.write("child_voice.wav",  data)
        showinfo("Başarılı", "Dosya çocuk sesine çevrildi.")

    # Çocuk sesi seçildi
    # Burada dosyanın çocuk sesine çevrilmesi işlemi yapılabilir
        
        
    elif secim == 2:
    # Kadın sesi seçildi
    # Burada dosyanın kadın sesine çevrilmesi işlemi yapılabilir
        showinfo("Başarılı", "Dosya kadın sesine çevrildi.")
        pass
"""


#    Bu fonksiyonu çalıştırmak için, "Çalıştır" butonuna bir command parametresi eklemeniz gerekiyor:

    calistir_button = Button(frame_alt_sol, text="Çalıştır", command=calistir)
    calistir_button.pack(anchor=S)
    
    
    
    
    


        
Label(frame_alt_sag, text="Ses diagramı",
      bg='#add8e6', font="Verdan 12 bold").pack()

metin_alani = Text(frame_alt_sag, height=9, width=45)
metin_alani.tag_configure('stil', foreground="#bfbfbf",
                          font=('Verdana', 7, 'bold'))
metin_alani.pack()



calistir_button= Button(frame_alt_sol, text="Çalıstır",command=calistir)# eğer calistir butonuna basıınca ekranın gitmesini istiyorsan command=master.destroy yap
calistir_button.pack(anchor=S)


master.mainloop()  # mainloop sayesinde arayüz devamlı ekranda kalıyor





