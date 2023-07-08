import socket
import pyaudio
import numpy as np
import threading
import tkinter as tk
from scipy import signal 


class SesIletisimArayuzuE:
    def __init__(self):
        self.HOST = 'SERVER_IP_ADRESS' 
        self.PORT = 12345
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 22050
        self.PITCH_SHIFT_FACTOR = 1.2

        self.event = threading.Event()

        self.server_socket = None
        self.client_socket = None
        self.stream = None
        self.speaker_stream = None
        self.root = None

        self.is_running = False
        self.is_running_recv = True
        self.create_interface()
                            ##### ********** ######
    def create_interface(self):
        self.root = tk.Tk()
        self.root.title("Ses İletişim Arayüzü")
        self.root.geometry("250x230")

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
        
        
        
        
        
        p = pyaudio.PyAudio()
        self.stream = None
        self.stop_event = threading.Event()

        self.root = tk.Tk()
        self.root.title("Mikrofon Çıkışı Değiştirici")
        self.root.geometry("280x300")

        self.output_device_list = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                device_name = device_info["name"]
                self.output_device_list.append((i, device_name))
                if len(self.output_device_list) == 6:
                    break
        self.output_device_list = tuple(self.output_device_list)
        
        self.output_device_label = tk.Label(self.root, text="Ses Çıkışı:")
        self.output_device_label.pack()

        self.output_device_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE,height=13,width=30)
        self.output_device_listbox.pack()
        
        for device in self.output_device_list:
            self.output_device_listbox.insert(tk.END, device[1])

        self.select_button = tk.Button(self.root, text="Seç", command=self.play_button_clicked)
        self.select_button.pack()

        self.stop_button = tk.Button(self.root, text="Durdur", command=self.stop_button_clicked)
        self.stop_button.pack()
        
                            ##### ********** ######
    def send_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
       
        
        while self.is_running:
            try:
                    
                data = stream.read(self.CHUNK)
                audio_data = np.frombuffer(data, dtype=np.int16)
            
                converted_data= signal.resample(audio_data,int(len(audio_data)*self.PITCH_SHIFT_FACTOR))*1.4
                converted_data = converted_data.astype(np.int16)
                converted_data_bytes = converted_data.tobytes()
                self.client_socket.send(converted_data_bytes)
                
           
                if not self.is_running:
                    break
            except Exception as e:
                print("bir hata oldu : ",e)
                print("yeniden bağlanılmaya çalışılıyor...")
                self.client_socket.close()
                self.client_socket, address = self.server_socket.accept()
                print(f"* {address} adresinden yeni bir bağlantı alındı.")

                
                data = stream.read(self.CHUNK)
                audio_data = np.frombuffer(data, dtype=np.int16)
            
                converted_data= signal.resample(audio_data,int(len(audio_data)*self.PITCH_SHIFT_FACTOR))*1.4
                converted_data = converted_data.astype(np.int16)
                converted_data_bytes = converted_data.tobytes()
                self.client_socket.send(converted_data_bytes)
                
           
                if not self.is_running:
                    break


        
        stream.stop_stream()
        stream.close()
        p.terminate()
                            ##### ********** ######            
    """ def determine_gender(self,audio_data ):
        if np.mean(audio_data) > 0:
            gender = "female"
        else:
            gender = "male"
        
        return gender        """
        
                            ##### ********** ######
    def get_sound_fonc(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.CHANNELS,
            rate=self.RATE,
            output=True
        )

        while self.is_running_recv:
            try:
                data = self.client_socket.recv(self.CHUNK)
                if not data:
                    break
                if self.event.is_set():
                    self.play_server_output(data)
            except Exception as e:
                print("Beklenmeyen bir hata oluştu:", e)
                print("Yeni bir bağlantı bekleniyor...")
                self.client_socket.close()
                self.client_socket, address = self.server_socket.accept()
                print(f"* {address} adresinden yeni bir bağlantı alındı.")
                
                data = self.client_socket.recv(self.CHUNK)
                if not data:
                    break
                if self.event.is_set():
                    self.play_server_output(data)

        stream.stop_stream()
        stream.close()
        self.client_socket.close()
        p.terminate()
                            ##### ********** ######        
    def start_get_sound(self):
        threading.Thread(target=self.get_sound_fonc).start()
        self.get_sound_button.config(state="disabled" )

                            ##### ********** ######

    def get_sound_stop(self):
        self.event.clear()
        #self.is_running_recv = False
        self.get_sound_stop_button.config(state="disabled")
        self.get_sound_contunie_button.config(state="active")
                            ##### ********** ######
    def get_sound_contunie(self):
        self.event.set()
        self.get_sound_contunie_button.config(state="disabled")
        self.get_sound_stop_button.config(state="active")
        
                            ##### ********** ######
    def start(self):
        self.is_running = True
        threading.Thread(target=self.send_audio).start()
                            ##### ********** ######
    def stop(self):
        self.is_running = False

                            ##### ********** ######
    def klavye_kontrol(self, event):
        if event.char == 'q':
            if event.type == tk.EventType.KeyPress:
                self.start()
            elif event.type == tk.EventType.KeyRelease:
                self.stop()
                             ##### ********** ###### 
    def set_output_stream(self, output_device):
        p = pyaudio.PyAudio()
       
        self.output_stream = p.open(
            output=True,
            format=pyaudio.paInt16,
            channels=self.CHANNELS,
            rate=self.RATE,
            frames_per_buffer=self.CHUNK,
            output_device_index=output_device,
        )
                            ##### ********** ######
    def play_server_output(self, data):
        self.output_stream.write(data)
                            ##### ********** ######
    def select_output_device(self):
        device_index = self.output_device_listbox.curselection()
        output_device = self.output_device_list[device_index[0]][0]
        return output_device
                            ##### ********** ######
    def play_button_clicked(self):
        output_device = self.select_output_device()
        self.stop_event.clear()
        self.set_output_stream(output_device)
        #self.play_server_output(data)
                            ##### ********** ######
    def stop_button_clicked(self):
        self.stop_event.set()
        
                             ##### ********** ######   
    def run_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(1)

        print(f"* Bağlantı için {self.HOST}:{self.PORT} dinleniyor...")

        self.client_socket, address = self.server_socket.accept()
        print(f"* {address} adresinden bir bağlantı alındı.")

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

        speaker_stream = p.open(format=pyaudio.paInt16,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    output=True)

        self.root.mainloop()

        stream.stop_stream()
        stream.close()
        speaker_stream.stop_stream()
        speaker_stream.close()
        p.terminate()

        self.client_socket.close()
        self.server_socket.close()


if __name__ == "__main__":
    ses_arayuzu = SesIletisimArayuzuE()
    ses_arayuzu.run_server()
    
