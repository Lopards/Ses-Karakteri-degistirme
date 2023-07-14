import tkinter as tk
import tkinter.ttk as ttk
import threading
import pyaudio
import numpy as np
import socket
import subprocess

class Client:
    def __init__(self):
        self.CHUNK = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 22050

        self.HOST = None  # Sunucu IP adresi
        self.PORT = 12345  # Sunucu port numarası
        self.contunie = True
        self.is_running = False
        self.is_running_recv = True

        self.event = threading.Event()

        self.server_socket = None
        self.stream = None
        self.root = None

        self.ip_file = "ip_addresses.txt"  # IP adreslerini saklayan dosya adı

        self.create_interface()

    def create_interface(self):
        self.root = tk.Tk()
        self.root.title("Ses İletişim Arayüzü")
        self.root.geometry("400x250")

        self.ip_label = tk.Label(self.root, text="IP Adresi:")
        self.ip_label.pack()

        self.ip_combobox = ttk.Combobox(self.root, values=self.get_saved_ip_addresses())
        self.ip_combobox.pack()

        self.scan_ip_button = tk.Button(self.root, text="İP TARA", command=self.scan_ip)
        self.scan_ip_button.pack()

        self.connect_button = tk.Button(self.root, text="Bağlan", command=self.connect_to_server)
        self.connect_button.pack()

        self.start_button = tk.Button(self.root, text="Başlat", command=self.start_communication, state="disabled")
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Durdur", command=self.stop_communication, state="disabled")
        self.stop_button.pack()

        self.get_sound_button = tk.Button(self.root, text="Ses Al", command=self.get_sound, state="disabled")
        self.get_sound_button.pack()

        self.get_sound_continue_button = tk.Button(self.root, text="Ses Almaya Devam Et", command=self.get_sound_continue, state="disabled")
        self.get_sound_continue_button.pack()

        self.get_sound_stop_button = tk.Button(self.root, text="Ses Almayı Durdur", command=self.get_sound_stop, state="disabled")
        self.get_sound_stop_button.pack()

        self.disconnect_button = tk.Button(self.root, text="Bağlantıyı kes", command=self.disconnect, state="disabled")
        self.disconnect_button.pack()

        self.root.mainloop()

    def scan_ip(self):
        output = subprocess.check_output(['nmap', '-sn', '192.168.1.0/24'])
        output = output.decode('latin-1')

        print("Ağdaki tüm cihazların IP adresleri:")
        lines = output.splitlines()
        for line in lines:
            if 'Nmap scan report for' in line:
                ip_address = line.split()[-1]
                print(ip_address) # şu anda sadece terminale yazdırıyor.


    def connect_to_server(self):
        selected_ip = self.ip_combobox.get()
        self.HOST = selected_ip

        if selected_ip not in self.get_saved_ip_addresses():
            self.save_ip_address(selected_ip)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.HOST, self.PORT))
        print(f"Bağlantı sağlandı: {self.HOST}")

        self.start_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.get_sound_button.config(state="normal")
        self.disconnect_button.config(state="normal")

    def disconnect(self):
        self.is_running = False  # Gönderim ve ses alma işlemlerini durdur
        self.is_running_recv = False
        self.contunie = False # bağlantı yönetimi için
        
        
        if self.server_socket is not None:
            self.server_socket.close()
        
        self.root.quit()

    def start_communication(self):
        if not self.is_running:
            self.is_running = True
            threading.Thread(target=self.send_audio).start()

    def get_sound(self):
        self.is_running_recv = True
        threading.Thread(target=self.receive_audio).start()
        self.get_sound_button.config(state="disabled")
        self.get_sound_continue_button.config(state="normal")

    def get_sound_stop(self):
        self.event.clear()
        self.get_sound_stop_button.config(state="disabled")
        self.get_sound_continue_button.config(state="normal")

    def get_sound_continue(self):
        self.event.set()
        self.get_sound_continue_button.config(state="disabled")
        self.get_sound_stop_button.config(state="normal")

    def stop_communication(self):
        if self.is_running :    
            self.is_running = False

    def send_audio(self):
        p = pyaudio.PyAudio()

        self.stream = p.open(format=pyaudio.paInt16,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)

        while self.is_running:
            try:
                data = self.stream.read(self.CHUNK)
                audio_data = np.frombuffer(data, np.int16)
                self.server_socket.sendall(audio_data)

                if not self.is_running:
                    break
            except Exception as e:
                print("Beklenmedik bir hata oluştu...Lutfen bekleyiniz:  ",e)
                print("yeniden bağlanılmaya çalışılıyor.")
                #.server_socket.close()
                self.connect_to_server()
                p = pyaudio.PyAudio()

                self.stream = p.open(format=pyaudio.paInt16,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)
                
                data = self.stream.read(self.CHUNK)
                audio_data = np.frombuffer(data, np.int16)
                self.server_socket.sendall(audio_data)

                if not self.is_running:
                    break

        self.stream.stop_stream()
        self.stream.close()
        p.terminate()

    def receive_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True)

        while self.is_running_recv:
            try:
                data = self.server_socket.recv(self.CHUNK)

                if not data:
                    break

                if self.event.is_set() and self.contunie:
                    stream.write(data)
            except Exception as e:
                if self.server_socket is not None and self.contunie:
                    print("Bağlantı sıfırlandı... Yeniden bağlanılıyor.\ne")
                    self.connect_to_server()
                    data = self.server_socket.recv(self.CHUNK)

                    if not data:
                        break

                    if self.event.is_set():
                        stream.write(data)
        

        stream.stop_stream()
        stream.close()
        p.terminate()


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

if __name__ == "__main__":
    client = Client()
