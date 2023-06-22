import socket
import pyaudio
import numpy as np
import threading
import tkinter as tk
from scipy import signal 



class SesIletisimArayuzuK:
    def __init__(self):
        self.HOST = '192.168.1.44'
        self.PORT = 12345
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 22050
        self.PITCH_SHIFT_FACTOR = 0.85

        self.event = threading.Event()

        self.server_socket = None
        self.client_socket = None
        self.stream = None
        self.speaker_stream = None
        self.root = None

        self.is_running = False
        self.is_running_recv = True
        self.create_interface()

    def create_interface(self):
        self.root = tk.Tk()
        self.root.title("Ses İletişim Arayüzü")

        self.start_button = tk.Button(
            self.root, text="Başlat", command=self.start)
        self.start_button.pack()

        self.stop_button = tk.Button(
            self.root, text="stop", command=self.stop)
        self.stop_button.pack()

        self.get_sound_button = tk.Button(
            self.root, text="Ses Al", command=self.start_get_sound)
        self.get_sound_button.pack()
        
        self.get_sound_stop_button = tk.Button(
        self.root, text="Ses Alı Duraklat", command=self.get_sound_stop)
        self.get_sound_stop_button.pack()

        self.get_sound_contunie_button = tk.Button(
        self.root, text="Ses Alı Devam Et", command=self.get_sound_contunie)
        self.get_sound_contunie_button.pack()       
        
        
        self.root.bind("<KeyPress>", self.klavye_kontrol)
        self.root.bind("<KeyRelease>", self.klavye_kontrol)
        

    def send_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
       
        
        while self.is_running:
            data = stream.read(self.CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            converted_data= signal.resample(audio_data,int(len(audio_data)*self.PITCH_SHIFT_FACTOR))*1.3
            converted_data = converted_data.astype(np.int16)
            converted_data_bytes = converted_data.tobytes()
            self.client_socket.sendall(converted_data_bytes)
            
           
            if not self.is_running:
                break
        
        stream.stop_stream()
        stream.close()
        p.terminate()

    
    """   
    def determine_gender(self,audio_data ):
        if np.mean(audio_data) > 0:
            gender = "female"
        else:
            gender = "male"
        
        return gender        """

    def get_sound_fonc(self):
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            output=True)

        while self.is_running_recv:
            data = self.client_socket.recv(self.CHUNK)
            if not data:
                break
            if self.event.is_set():
                self.stream.write(data)

        self.stream.stop_stream()
        self.stream.close()
        self.client_socket.close()
        p.terminate()
        
    def start_get_sound(self):
        threading.Thread(target=self.get_sound_fonc).start()
        self.get_sound_button.config(state="disabled" )



    def get_sound_stop(self):
        self.event.clear()
        #self.is_running_recv = False
        self.get_sound_stop_button.config(state="disabled")
        self.get_sound_contunie_button.config(state="active")

    def get_sound_contunie(self):
        self.event.set()
        self.get_sound_contunie_button.config(state="disabled")
        self.get_sound_stop_button.config(state="active")
        


    def start(self):
        self.is_running = True
        threading.Thread(target=self.send_audio).start()

    def stop(self):
        self.is_running = False


    def klavye_kontrol(self, event):
        if event.char == 'q':
            if event.type == tk.EventType.KeyPress:
                self.start()
            elif event.type == tk.EventType.KeyRelease:
                self.stop()

    def run_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(1)

        print(f"* Bağlantı için {self.HOST}:{self.PORT} dinleniyor...")

        self.client_socket, address = self.server_socket.accept()
        print(f"* {address} adresinden bir bağlantı alındı.")

        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

        self.speaker_stream = p.open(format=pyaudio.paInt16,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    output=True)




        self.root.mainloop()

        self.stream.stop_stream()
        self.stream.close()
        self.speaker_stream.stop_stream()
        self.speaker_stream.close()
        p.terminate()

        self.client_socket.close()
        self.server_socket.close()


if __name__ == "__main__":
    ses_arayuzu = SesIletisimArayuzuK()
    ses_arayuzu.run_server()
