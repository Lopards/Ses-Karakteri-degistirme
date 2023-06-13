import socket
import pyaudio
import numpy as np
from scipy import signal
import threading
import tkinter as tk

# class eklenen kod
"""
arayüz başladıktan sonra BAS-KONUŞ özelliğini aktif etmek isterseniz "q" tuşuna basiniz.
"""
class Server:
    def __init__(self):
        # PyAudio ayarları
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 22050

        # Bağlantı ve soket ayarları
        self.HOST = 'YOUR_IP_NUMBER'
        self.PORT = 12345

        # Pitch değiştirme faktörü
        self.PITCH_SHIFT_FACTOR = 0.85

        self.is_running = False
        self.is_paused = False
        self.server_socket = None
        self.client_socket = None
        self.stream = None
        self.speaker_stream = None
        self.thread = None

        self.create_interface()

    def create_interface(self):
        self.root = tk.Tk()
        self.root.title("Ses İletişim Arayüzü")

        self.start_button = tk.Button(self.root, text="Başlat", command=self.baslat)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Durdur", command=self.durdur)
        self.stop_button.pack()

        self.root.bind("<KeyPress>", self.klavye_kontrol)
        self.root.bind("<KeyRelease>", self.klavye_kontrol)

    def baslat(self):
        self.is_running = True
        threading.Thread(target=self.donustur_ve_gonder).start()

    def durdur(self):
        self.is_running = False

    def klavye_kontrol(self, event):
        if event.char == 'q':
            if event.type == tk.EventType.KeyPress:
                self.donustur_ve_gonder()
            elif event.type == tk.EventType.KeyRelease:
                self.durdur()

    def donustur_ve_gonder(self):
        while True:
            data = self.stream.read(self.CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
           
            if np.mean(audio_data) > 0:
                cinsiyet = "kadın"
            else:
                cinsiyet = "erkek"
            
            
            if cinsiyet == "kadın":
                self.client_socket.sendall(audio_data)
            elif cinsiyet == "erkek":
                converted_data = signal.resample(audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR)) * 1.4
                converted_data = converted_data.astype(np.int16)
                converted_data_bytes = converted_data.tobytes()
                self.client_socket.sendall(converted_data_bytes)

            if not self.is_running:
                break


    def run(self):
        # Soket oluşturma ve bağlantıyı bekletme
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(1)

        print(f"* Bağlantı için {self.HOST}:{self.PORT} dinleniyor...")

        self.client_socket, address = self.server_socket.accept()
        print(f"* {address} adresinden bir bağlantı alındı.")

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        self.speaker_stream = self.p.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          output=True)

        self.root.mainloop()

        self.stream.stop_stream()
        self.stream.close()
        self.speaker_stream.stop_stream()
        self.speaker_stream.close()
        self.p.terminate()

        self.client_socket.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = Server()
    server.run()
