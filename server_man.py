import socket
import pyaudio
import numpy as np
from scipy import signal
import threading
import tkinter as tk

# PyAudio ayarları
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050

# Bağlantı ve soket ayarları
HOST = '192.168.1.44'
PORT = 12345

# Pitch değiştirme faktörü
PITCH_SHIFT_FACTOR = 1.2



# Soket oluşturma ve bağlantıyı bekletme
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"* Bağlantı için {HOST}:{PORT} dinleniyor...")

client_socket, address = server_socket.accept()
print(f"* {address} adresinden bir bağlantı alındı.")

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

speaker_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True)



# Ses dönüşümü ve gönderme
def convert_and_send(stream, speaker_stream):
    while True:
        data = stream.read(CHUNK)
        
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        gender = determine_gender(audio_data)
        print(gender)
        if gender == "man":
            client_socket.sendall(audio_data)
        else:
            converted_data = signal.resample(audio_data, int(len(audio_data) * PITCH_SHIFT_FACTOR)) * 1.4
            converted_data = converted_data.astype(np.int16)
            converted_data_bytes = converted_data.tobytes()
            client_socket.sendall(converted_data_bytes)
        
        if not is_running:
            break

def determine_gender(audio_data):
    if np.mean(audio_data) > 0:
        gender = "woman"
    else:
        gender = "man"
    
    return gender






def klavye_kontrol(self, event):
        if event.char == 'q':
            if is_running and not self.is_paused:
                is_paused = True
            elif self.is_running and self.is_paused:
                self.is_paused = False
                self.bas_konus()

def bas_konus(self):
        if threading.Thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=convert_and_send)
            self.thread.start()



# Arayüz buton işlevleri
def start():
    global is_running
    is_running = True
    threading.Thread(target=convert_and_send, args=(stream, speaker_stream)).start()

def stop():
    global is_running
    is_running = False

def bas_konus(event):
    if event.type == tk.EventType.KeyDown and event.keysym == "k":
        threading.Thread(target=convert_and_send, args=(stream, speaker_stream)).start()

# Arayüz oluşturma
root = tk.Tk()
root.title("Ses İletişim Arayüzü")

start_button = tk.Button(root, text="Başlat", command=start)
start_button.pack()

stop_button = tk.Button(root, text="Durdur", command=stop)
stop_button.pack()

press_Speak_button = tk.Button(root, text="Bas-Konus", command=bas_konus)
press_Speak_button.pack()
root.bind("<KeyPress>", bas_konus)
root.bind("<KeyRelease>", bas_konus)

root.mainloop()

stream.stop_stream()
stream.close()
speaker_stream.stop_stream()
speaker_stream.close()
p.terminate()

client_socket.close()
server_socket.close()