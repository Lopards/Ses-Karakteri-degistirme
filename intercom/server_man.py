import socket
import pyaudio
import numpy as np
from scipy import signal
# instant male voice change

# PyAudio ayarları
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Bağlantı ve soket ayarları
HOST = 'YOUR_IP_ADRESS' 
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

# Ses dönüşümü ve gönderme
def convert_and_send(stream, speaker_stream):
    while True:
        data = stream.read(CHUNK)
        
        audio_data = np.frombuffer(data, dtype=np.int16)
     
        converted_data = signal.resample(audio_data, int(len(audio_data) * PITCH_SHIFT_FACTOR))*1.4
        converted_data = converted_data.astype(np.int16)
        converted_data_bytes = converted_data.tobytes()
        client_socket.sendall(converted_data_bytes)
       # speaker_stream.write(data)  # Dönüştürülmemiş sesi hoparlörden çal
            
"""""
def determine_gender(data):
    if np.mean(data) > 0:
        gender = "woman"
    else:
        gender = "man"
    
    return gender
"""""


# PyAudio stream oluşturma mic hoparlör
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Hoparlör için PyAudio stream oluşturma
speaker_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True)

print("* Ses kaydediliyor ve dönüştürülerek gönderiliyor...")
convert_and_send(stream, speaker_stream)

stream.stop_stream()
stream.close()
speaker_stream.stop_stream()
speaker_stream.close()
p.terminate()

client_socket.close()
server_socket.close()