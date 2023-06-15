import socket
import pyaudio
import numpy as np
import tkinter as tk
import threading


class Client:
    def _init_(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 22050

        self.HOST = 'server_ip'  # Sunucu IP adresi
        self.PORT = 12345  # Sunucu port numarası

        self.is_running = False
        self.server_socket = None
        self.stream = None
        self.root = None

        self.create_interface()

    def create_interface(self):
        self.root = tk.Tk()
        self.root.title("Ses İletişim Arayüzü")

        self.start_button = tk.Button(
            self.root, text="Başlat", command=self.start_communication)
        self.start_button.pack()

        self.stop_button = tk.Button(
            self.root, text="Durdur", command=self.stop_communication)
        self.stop_button.pack()

        self.sesal = tk.Button(self.root, text="ses-al", command=self.ses_al)
        self.sesal.pack()

        self.sesal_stop = tk.Button(
            self.root, text="ses-al-stop", command=self.ses_al_stop)
        self.sesal_stop.pack()

        self.root.bind("<KeyPress>", self.keyboard_control)
        self.root.bind("<KeyRelease>", self.keyboard_control)

    def start_communication(self):
        self.is_running = True
        threading.Thread(target=self.send_audio).start()

    def ses_al(self):
        self.is_running = True
        threading.Thread(target=self.receive_audio,
                         args=self.is_running).start()

    def ses_al_stop(self):
        self.is_running = False

    def stop_communication(self):
        self.is_running = False

    def keyboard_control(self, event):
        if event.char == 'q':
            if event.type == tk.EventType.KeyPress:
                self.send_audio()
            elif event.type == tk.EventType.KeyRelease:
                self.stop_communication()

    def send_audio(self):
        p = pyaudio.PyAudio()
        self.stream = p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)

        while self.is_running:
            data = self.stream.read(self.CHUNK)
            audio_data = np.frombuffer(data, np.int16)
            self.server_socket.sendall(audio_data)

            if not self.is_running:
                break

        self.stream.stop_stream()
        self.stream.close()
        p.terminate()

    def receive_audio(self, is_running):
        p = pyaudio.PyAudio()
        speaker_stream = p.open(format=self.FORMAT,
                                channels=self.CHANNELS,
                                rate=self.RATE,
                                output=True)

        while True:
            if is_running:
                data = self.server_socket.recv(self.CHUNK)
                if not data:
                    break
                speaker_stream.write(data)

            else:
                break

        speaker_stream.stop_stream()
        speaker_stream.close()
        p.terminate()

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.HOST, self.PORT))

        self.root.mainloop()
        self.server_socket.close()


if __name__ == "__main__":
    client = Client()
    client.run()
