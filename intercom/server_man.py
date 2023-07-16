import socket
import pyaudio
import numpy as np
import threading
import tkinter as tk
import tkinter.ttk as ttk
from scipy import signal 
from urllib import request


# ani program kapanmasına karşılık try-expect eklendi.
#hoparlör
class SesIletisimArayuzuE:
    def __init__(self):
        self.HOST = None
        self.PORT = 12345
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 22050
        self.PITCH_SHIFT_FACTOR = 1.2

        self.event = threading.Event()
        self.contunie = True
        self.server_socket = None
        self.client_socket = None
        self.stream = None
        self.output_stream = None
        self.speaker_stream = None
        self.root = None
        self.ip_file = "ip_addresses.txt"

        self.is_running = False
        self.is_running_recv = True
        self.create_interface()
                            ##### ********** ######
    def create_interface(self):
        self.root = tk.Tk()
        self.root.title("Ses İletişim Arayüzü")
        self.root.geometry("250x250")

        self.ip_label = tk.Label(self.root, text="IP Adresi:")
        self.ip_label.pack()

        self.ip_combobox = ttk.Combobox(self.root, values=self.get_saved_ip_addresses())
        self.ip_combobox.pack()

        self.connect_button = tk.Button(self.root, text="Bağlan", command=self.connect_to_server)
        self.connect_button.pack()

        self.start_button = tk.Button(
            self.root, text="Başlat",cursor="hand2", command=self.start)
        self.start_button.pack(pady=3)

        self.stop_button = tk.Button(
            self.root, text="stop",cursor="hand2", command=self.stop)
        self.stop_button.pack()

        self.get_sound_button = tk.Button(
            self.root, text="Ses Al",cursor="hand2", command=self.start_get_sound,disabledforeground="#a9a9a9")
        self.get_sound_button.pack(pady=3)
        
        self.get_sound_contunie_button = tk.Button(
        self.root, text="Ses Alı Devam Et",cursor="hand2", command=self.get_sound_contunie)
        self.get_sound_contunie_button.pack()  
        
        self.get_sound_stop_button = tk.Button(
        self.root, text="Ses Alı Duraklat",cursor="hand2", command=self.get_sound_stop)
        self.get_sound_stop_button.pack(pady=3)

        self.disconnect_button = tk.Button(
        self.root, text="Bağlantıyı kes",cursor="hand2", command=self.disconnect)
        self.disconnect_button.pack()  

             
        
        
        self.root.bind("<KeyPress>", self.klavye_kontrol)
        self.root.bind("<KeyRelease>", self.klavye_kontrol)
        
        
        
        
        
        p = pyaudio.PyAudio()
        self.stream = None
        self.stop_event = threading.Event()

        self.pencere = tk.Tk()
        self.pencere.title("hoparlör Çıkışı Değiştirici")
        self.pencere.geometry("280x300+450+100")
        

        self.output_device_list = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                device_name = device_info["name"]
                self.output_device_list.append((i, device_name))
                if len(self.output_device_list) == 6:
                    break
        self.output_device_list = tuple(self.output_device_list)
        
        self.output_device_label = tk.Label(self.pencere, text="Ses Çıkışı:")
        self.output_device_label.pack()

        self.output_device_listbox = tk.Listbox(self.pencere, selectmode=tk.SINGLE,height=13,width=30)
        self.output_device_listbox.pack()
        
        for device in self.output_device_list:
            self.output_device_listbox.insert(tk.END, device[1])

        self.select_button = tk.Button(self.pencere, text="Seç", command=self.play_button_clicked,cursor="hand2",activeforeground="red")
        self.select_button.pack()

        """self.stop_button = tk.Button(self.pencere, text="Durdur",cursor="hand2",command=self.stop_button_clicked)
        self.stop_button.pack()"""

        self.root.mainloop()
        self.pencere.mainloop()
        
                            ##### ********** ######

    def connect_to_server(self):
        selected_ip = self.ip_combobox.get()
        self.HOST = selected_ip

        if selected_ip not in self.get_saved_ip_addresses():
            self.save_ip_address(selected_ip)
        
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

    def disconnect(self):
        self.is_running = False  # Gönderim ve ses alma işlemlerini durdur
        self.is_running_recv = False
        self.contunie = False
        
        if self.client_socket is not None:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        if self.server_socket is not None:
            self.server_socket.close()
        
        self.root.quit()
        

  
        
    
    def get_saved_ip_addresses(self):
        ip_addresses = []
        try:
            with open(self.ip_file, "r") as f:
                for line in f:
                    ip_addresses.append(line.strip())
        except FileNotFoundError:
            pass
        return ip_addresses

    def save_ip_address(self, ip_address):
        with open(self.ip_file, "a") as f:
            f.write(ip_address + "\n")
    

    def send_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
       
        
        while self.is_running:
            try:
                  while self.is_running:  
                    data = stream.read(self.CHUNK)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                
                    converted_data= signal.resample(audio_data,int(len(audio_data)*self.PITCH_SHIFT_FACTOR))*1.4
                    converted_data = converted_data.astype(np.int16)
                    converted_data_bytes = converted_data.tobytes()
                    self.client_socket.send(converted_data_bytes)
                    
            
                    if not self.is_running:
                        return
            except Exception as e:
                if self.client_socket is not None and self.contunie == True:
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
                        return


        
        stream.stop_stream()
        stream.close()
        self.client_socket.close()
        p.terminate()

    
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
                if self.event.is_set() and self.contunie:
                    self.play_server_output(data)
                else:
                    print("ses al devam tuşuna bas")
            except Exception as e:
                if self.client_socket is not None and self.contunie:
                    print("Beklenmeyen bir hata oluştu:", e)
                    print("Yeni bir bağlantı bekleniyor...")
                    self.client_socket.close()
                    self.client_socket = None  # client_socket nesnesini None olarak ayarlayın
                    
                    # Yeni bir bağlantı almak için yeni bir server_socket nesnesi oluşturun
                    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.server_socket.bind((self.HOST, self.PORT))
                    self.server_socket.listen(1)
                    print(f"* Bağlantı için {self.HOST}:{self.PORT} dinleniyor...")
                    
                    self.client_socket, address = self.server_socket.accept()
                    print(f"* {address} adresinden yeni bir bağlantı alındı.")
        
        stream.stop_stream()
        stream.close()
        self.client_socket.close()
        p.terminate()
                
            
        

        """stream.stop_stream()
            stream.close()
            self.client_socket.close()
            p.terminate()"""


                            ##### ********** ######        
    def start_get_sound(self):
        self.contunie = True
        
        self.is_running_recv = True
        threading.Thread(target=self.get_sound_fonc).start()
        self.get_sound_button.config(state="normal",cursor="arrow")

                            ##### ********** ######

    def get_sound_stop(self):
        self.event.clear()
        #self.is_running_recv = False
        self.get_sound_stop_button.config(state="disabled",cursor="arrow")
        self.get_sound_contunie_button.config(state="active",cursor="hand2")
                            ##### ********** ######
    def get_sound_contunie(self):
        self.event.set()
        self.get_sound_contunie_button.config(state="disabled",cursor="arrow")
        self.get_sound_stop_button.config(state="active",cursor="hand2")
        
                            ##### ********** ######
    def start(self):
        if not self.is_running:
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
        if self.output_stream is not None:
            try:
                self.output_stream.write(data)
            except OSError as e:
                print("Hoparlör bağlantısı koparıldı:", e)
                self.output_stream.close()
                self.output_stream.stop_stream()
                
                self.output_stream = None
                hoparlor = self.select_output_device()
                self.set_output_stream(hoparlor)
                
                
        else:
            print("Hoparlör seçiniz...")
            
                        ##### ********** ######
    def select_output_device(self):
        device_index = self.output_device_listbox.curselection()
        output_device = self.output_device_list[device_index[0]][0]
        return output_device

    def play_button_clicked(self):
        output_device = self.select_output_device()
        self.stop_event.clear()
        self.set_output_stream(output_device)
        #self.play_server_output(data)



    def connect(self):
        try:
            request.urlopen('http://google.com', timeout=1)
            return True
        except request.URLError as err: 
            return False

                            ##### ********** ######
    """def stop_button_clicked(self):
        self.stop_event.set()"""

    
                                     ##### ********** ######   


if __name__ == "__main__":
    ses_arayuzu = SesIletisimArayuzuE()
