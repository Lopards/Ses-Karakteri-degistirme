import socket
import pyaudio

# PyAudio ayarları
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050

# Bağlantı ayarları
HOST = 'IP_ADRESS'
PORT = 12345

# Soket bağlantısı ve ses alma
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("* Sunucuya bağlanıldı.")

# Ses oynatma
def play_sound(stream):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    while True:
        data = stream.recv(CHUNK)
        if not data:
            break
        stream.write(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Soket bağlantısı için PyAudio stream oluşturma
stream = client_socket.makefile('rb')

print("* Ses alındı ve oynatılıyor...")
play_sound(stream)

stream.close()
client_socket.close()
