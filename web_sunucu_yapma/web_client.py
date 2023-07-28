import requests
import threading
import tkinter as tk
from tkinter import scrolledtext

# Sunucu adresi
SERVER_ADDRESS = "http://192.168.1.53:8080/"

# Metin mesajı için değişken
mesaj = ""

def update_message():
    global mesaj
    while True:
        response = requests.get(SERVER_ADDRESS)
        if response.status_code == 200:
            yeni_mesaj = response.text
            if yeni_mesaj != mesaj:
                mesaj = yeni_mesaj
                root.after(100, update_text_mesaj)

def update_text_mesaj():
    text_mesaj.config(state=tk.NORMAL)
    text_mesaj.delete('1.0', tk.END)
    text_mesaj.insert(tk.END, mesaj)
    text_mesaj.config(state=tk.DISABLED)

if __name__ == '__main__':
    # Tkinter arayüzü oluştur
    root = tk.Tk()
    root.title("İstemci")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    text_mesaj = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED)
    text_mesaj.pack()

    # İstemci mesajları güncelleme thread'ini başlat
    update_thread = threading.Thread(target=update_message)
    update_thread.daemon = True
    update_thread.start()

    root.mainloop()
