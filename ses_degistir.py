from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.ttk import Combobox
from tkinter.messagebox import showinfo
from tkinter import messagebox

import Ses_Degistirme_fonk
import Ses_kaydedici


def dosya_sec():
    dosya_yolu = fd.askopenfilename(initialdir="/", title="Dosya Seç",
                                    filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    dosya_yolu_kiti.config(text="Dosya YOLU = " + dosya_yolu)
    

arayuz=Tk()
arayuz.title="Ses Degistime programi"
Canvas = Canvas(arayuz, height=450, width=750)
Canvas.pack()

frame_ustbolge=Frame(arayuz,bg="#0080FF")
frame_ustbolge.place(relx=0.1,rely=0.1,relwidth=0.75,relheight=0.1)

frame_altSol=Frame(arayuz,bg="#0080FF")
frame_altSol.place(relx=0.1, rely=0.21, relwidth=0.23, relheight=0.66)

frame_altSag=Frame(arayuz,bg="#0080FF")
frame_altSag.place(relx=0.34, rely=0.21, relwidth=0.51, relheight=0.66)

dosya_yolu_kiti = Label(frame_ustbolge, bg='#0080FF',
                        text="Dosya YOLU = ", font="Verdana 10 bold")
dosya_yolu_kiti.pack(padx=10, side=LEFT)

dosya_sec_button = Button(frame_ustbolge, text="Dosya Seç", command=dosya_sec)
dosya_sec_button.pack(padx=10, side=LEFT)


Label(frame_altSol,text="Hangi sesi istiyorsunuz?",bg="#0080FF",
      font="Verdan 9 bold").pack(padx=10, pady=10, anchor=NW)

var = IntVar()

S1 = Radiobutton(frame_altSol, text="Çocuk sesi", variable=var,
                 value=1, bg='#add8e6', font="Verdan 8")
S1.pack(padx=15, pady=5, anchor=NW)

S2 = Radiobutton(frame_altSol, text="Kadın sesi", variable=var,
                 value=2, bg='#add8e6', font="Verdan 8")
S2.pack(padx=15, pady=5, anchor=NW)

seskayitDurdur_button=Button(frame_ustbolge, text="Kayıt başlat- Durdur",command=Ses_kaydedici.SoundRecorderGUI)
seskayitDurdur_button.pack(padx=15,pady=10,side=RIGHT)


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

    ses_degistirici = Ses_Degistirme_fonk.Ses_Degistir(dosya_yolu)

    filtreli_data = ses_degistirici.pitch_shift(secim)

    if filtreli_data is not None:
        yeni_dosya = 'yeni_ses.wav'
        ses_degistirici.save_wav(yeni_dosya, filtreli_data)
        


calistir_button = Button(frame_altSol, text="Çalıstır", command=calistir)
calistir_button.pack(anchor=S)





arayuz.mainloop()

