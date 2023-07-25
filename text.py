# server_manVol2 de metin göndermek için ayrı bir socket yapısı kullanılacaktır.
import socket
import tkinter as tk
import threading
HOST = "192.168.1.48"
PORT = 12346


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"* Bağlantı için {HOST}:{PORT} dinleniyor...")

client_socket, address = server_socket.accept()
print(f"** {address} metin gönderimi için  bir bağlantı alındı.")





def yazi_gonder():

        metin = text_place.get("1.0", tk.END).strip()
        data = metin 
        if metin:
            client_socket.send(bytes(data,"utf-8"))
        else:
            print("bos metin göndermeye çalıştınız!!!")

def yazi_gonder_t():
     threading.Thread(target=yazi_gonder).start()
text_place = tk.Text(width=15,height=7)
text_place.pack()
send_button = tk.Button(text="gönder",command=yazi_gonder_t)
send_button.pack()
text_place.mainloop()