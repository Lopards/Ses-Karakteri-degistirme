import socket
import pyaudio
import numpy as np
"""from scipy import signal """  # eklenecek
import threading
import tkinter as tk


def donustur_ve_gonder(stream, client_socket, is_running, CHUNK, PITCH_SHIFT_FACTOR):
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        if is_running:
            client_socket.sendall(audio_data)
        else:
            break


def ses_al(stream, client_socket, CHUNK, is_running):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=22050, output=True, frames_per_buffer=CHUNK)

    while True:
        if is_running:
            data = client_socket.recv(CHUNK)
            if not data:
                break
            stream.write(data)
        else:
            break

    stream.stop_stream()
    stream.close()
    client_socket.close()
    p.terminate()


def run_server():
    HOST = 'SERVER_IP'
    PORT = 12345
    CHUNK = 1024
    PITCH_SHIFT_FACTOR = 1.2

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"* Bağlantı için {HOST}:{PORT} dinleniyor...")

    client_socket, address = server_socket.accept()
    print(f"* {address} adresinden bir bağlantı alındı.")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1, rate=22050,
                    input=True,
                    frames_per_buffer=CHUNK)

    speaker_stream = p.open(format=pyaudio.paInt16,
                            channels=1, rate=22050,
                            output=True)

    root = tk.Tk()
    root.title("Ses İletişim Arayüzü")

    def baslat():
        nonlocal is_running
        is_running = True
        threading.Thread(target=donustur_ve_gonder, args=(
            stream, client_socket, is_running, CHUNK, PITCH_SHIFT_FACTOR)).start()

    def ses_al_fonk():
        nonlocal is_running
        is_running = True
        threading.Thread(target=ses_al, args=(
            stream, client_socket, CHUNK, is_running)).start()

    def durdur():
        nonlocal is_running
        is_running = False

    def ses_al_stop():
        nonlocal is_running
        is_running = False

    is_running = False

    def klavye_kontrol(event):
        if event.char == 'q':
            if event.type == tk.EventType.KeyPress:
                donustur_ve_gonder(stream, client_socket,
                                   is_running, CHUNK, PITCH_SHIFT_FACTOR)
            elif event.type == tk.EventType.KeyRelease:
                durdur()

    root.bind("<KeyPress>", klavye_kontrol)
    root.bind("<KeyRelease>", klavye_kontrol)

    start_button = tk.Button(root, text="Başlat", command=baslat)
    start_button.pack()

    stop_button = tk.Button(root, text="Durdur", command=durdur)
    stop_button.pack()

    ses_al_button = tk.Button(root, text="ses-al", command=ses_al_fonk)
    ses_al_button.pack()

    ses_al_button_stop = tk.Button(
        root, text="ses-al-stop", command=ses_al_stop)
    ses_al_button_stop.pack()

    root.mainloop()

    stream.stop_stream()
    stream.close()
    speaker_stream.stop_stream()
    speaker_stream.close()
    p.terminate()

    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    run_server()
