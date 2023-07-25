import tkinter as tk
import socket
from clientV2 import Client
class Arayuz:
    def __init__(self):
        self.bilgisayarlar = {
            "Bilgisayar 1": "192.168.1.58",
            "Bilgisayar 2": "192.168.1.51",
            "Bilgisayar 3": "192.168.0.103"
        }

        self.pencere = tk.Tk()
        self.pencere.title("Bilgisayar Seç")
        self.pencere.geometry("300x200")

        self.bilgisayar_listesi = tk.Listbox(self.pencere)
        self.bilgisayar_listesi.pack(pady=10)

        self.baglanti_butonu = tk.Button(self.pencere, text="Bağlantı Kur", command=self.baglanti_kur)
        self.baglanti_butonu.pack()

        self.arayuz_guncelle()

        self.pencere.mainloop()

    def baglanti_kur(self):
        secili_bilgisayar = self.bilgisayar_listesi.get(tk.ACTIVE)
        ip_adresi = self.bilgisayarlar[secili_bilgisayar]

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip_adresi, 12345))
            print("Bağlantı başarılı!")
            # Bağlantı işlemlerini burada devam ettirebilirsiniz.
            ses = Client()
            ses.run()
        except ConnectionRefusedError:
            print("Bağlantı reddedildi!")

    def arayuz_guncelle(self):
        self.bilgisayar_listesi.delete(0, tk.END)
        for bilgisayar in self.bilgisayarlar:
            self.bilgisayar_listesi.insert(tk.END, bilgisayar)

if __name__ == "__main__":
    arayuz = Arayuz()

 