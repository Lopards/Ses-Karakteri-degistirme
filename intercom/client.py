import socket
import pyaudio
import numpy as np
import tkinter as tk
import threading


"RUN THİS CODE ON CLİENT COMPUTER İF YOU WANT INTERCOM"

class Client:
    def __init__ (self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 22050
        
        self.HOST = None
        self.PORT = 12345  # Sunucu port numarası

        self.is_running = False
        self.is_running_recv = True

        self.event = threading.Event()

        self.server_socket = None
        self.stream = None
        self.root = None

        self.create_interface()

    def create_interface(self):
        self.root = tk.Tk()
        self.root.title("Ses İletişim Arayüzü")

        self.ip_label = tk.Label(self.root, text="IP Adresi:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack()

        self.connect_button = tk.Button(self.root, text="Bağlan", command=self.connect_to_server)
        self.connect_button.pack()

        self.start_button = tk.Button(self.root, text="Başlat", command=self.start_communication)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Durdur", command=self.stop_communication)
        self.stop_button.pack()

        self.get_sound_button = tk.Button(self.root, text="ses-al", command=self.get_sound)
        self.get_sound_button.pack()

        self.get_sound_contunie_button = tk.Button(self.root, text="ses-al_devam", command=self.get_sound_contunie)
        self.get_sound_contunie_button.pack()

        self.get_sound_stop_button = tk.Button(self.root, text="ses-al-stop", command=self.get_sound_stop)
        self.get_sound_stop_button.pack()





     def connect_to_server(self):
        self.HOST = self.ip_entry.get()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.HOST, self.PORT))
        print(f"Bağlantı sağlandı: {self.HOST}")

        self.start_button.config(state="normal")
        self.get_sound_button.config(state="normal")   

    def start_communication(self):
        self.is_running = True
        threading.Thread(target=self.send_audio).start()

     

    def get_sound(self):
       
        self.is_running_recv = True
        threading.Thread(target=self.receive_audio).start()
        self.get_sound_button.config(state="disabled")

   
    
    def get_sound_stop(self):
        self.event.clear()

        self.get_sound_stop_button.config(state="disabled")
        self.get_sound_contunie_button.config(state="active")


    def get_sound_contunie(self):
        self.event.set()
        self.get_sound_contunie_button.config(state="disabled")
        self.get_sound_stop_button.config(state="active")

    def stop_communication(self):
        self.is_running = False

    

    def send_audio(self):
        p = pyaudio.PyAudio()
        
        stream = p.open(format=pyaudio.paInt16,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)

       

        while self.is_running:
            data = stream.read(self.CHUNK)
            audio_data = np.frombuffer(data,np.int16)
            self.server_socket.sendall(audio_data)

            if not self.is_running:
                break

        

        stream.stop_stream()
        stream.close()
        p.terminate()

    def receive_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                                channels=self.CHANNELS,
                                rate=self.RATE,
                                output=True)

        while self.is_running_recv:
                data = self.server_socket.recv(self.CHUNK)
             
                if not data:
                    break
                if self.event.is_set():
                    
                     stream.write(data)

        stream.stop_stream()
        stream.close()
        self.server_socket.close()
        p.terminate()


    """def determine_gender(self,data):
        if np.mean(data)>0:
            gender = "female"
        else:
            gender ="male"

        return gender"""
                        

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.HOST, self.PORT))
        print(f"bağlanıldı: {self.HOST}")

        self.root.mainloop()

        self.server_socket.close()


if __name__ == "__main__":
    client = Client()
    
