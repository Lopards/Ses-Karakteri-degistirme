from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import threading
import tkinter as tk
from tkinter import messagebox
# şu anda bu sunucudan istemciye metin gönderilebiliyor...
# Sunucu 
HOST_NAME = socket.gethostname()
PORT_NUMBER = 8080

# Metin mesajı için değişken
mesaj = ""

class server(BaseHTTPRequestHandler):
    def do_GET(self):
        global mesaj
        if self.path == '/':
            self.send_response(200) # başarı kodu =200ok
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = mesaj
            self.wfile.write(response.encode())

def start_server():
    server_address = (HOST_NAME, PORT_NUMBER)
    httpd = HTTPServer(server_address, server)
    print(f"Sunucu {HOST_NAME}:{PORT_NUMBER} adresinde çalışıyor...")
    httpd.serve_forever() #serverin kod kapanıncaya kadar açık durması için

def send_message():
    global mesaj
    mesaj = entry_mesaj.get("1.0",tk.END)
    entry_mesaj.delete("1.0", tk.END)
    
if __name__ == '__main__':
    #arayülz
    root = tk.Tk()
    root.title("Sunucu")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label_mesaj = tk.Label(frame, text="Metin:")
    label_mesaj.pack(side=tk.LEFT)

    entry_mesaj = tk.Text(frame, height=8,width=12)
    entry_mesaj.pack(side=tk.LEFT)

    button_gonder = tk.Button(frame, text="Gönder", command=send_message)
    button_gonder.pack(side=tk.LEFT)

    # Sunucu thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    root.mainloop()
