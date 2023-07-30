
from tkinter import *
import tkinter.ttk as ttk
import threading
import pyaudio
import numpy as np
import socket
import nmap
import tkinter as tk
import os
from gtts import gTTS
import pygame
from responsive_voice import ResponsiveVoice

class Client:
    def __init__(self):
        self.CHUNK = 512 
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 22050

        self.HOST = None  # Sunucu IP adresi
        self.PORT = 12345  # Sunucu port numarası
        self.PORT_TEXT = 12346
        self.contunie = True
        self.is_running = False
        self.is_running_recv = True
        self.is_reading = False
        self.thread = None

        self.event = threading.Event()

        self.server_socket = None
        self.stream = None
        self.root = None

        self.ip_file = "ip_addresses.txt"  # IP adreslerini saklayan dosya adı

        self.create_interface()

    def create_interface(self):
        self.root = tk.Tk()
        self.root.title("deneme")
        self.root.geometry("600x450")
        
        frame_sol = Frame(self.root )
        frame_sol.place(relx=0.03, rely=0.03, relwidth=0.55, relheight=0.55)

        frame_orta = Frame(self.root )
        frame_orta.place(relx=0.60,rely=0.03, relwidth=0.30, relheight=0.55)

        frame_alt = Frame(self.root)
        frame_alt.place(relx=0.15,rely=0.60, relwidth=0.70, relheight=0.36)
        
        self.ip_combobox = ttk.Combobox(frame_sol)
        self.ip_combobox.pack()
        
        self.listbox = tk.Listbox(frame_sol,height=10,width=50)
        self.listbox.pack()
        self.listbox.bind("<Double-Button-1>", self.handle_listbox_double_click) # çift tıklandığında combobox'a yönlendiriyor.
        
        self.metin_yeri = tk.Text(frame_alt,height=8,width=45)
        self.metin_yeri.pack()
        #self.metin_al_f = tk.Button(frame_alt, text="metin al",command=self.receive_text_thread, state="disabled")
        #self.metin_al_f.pack()

        """self.read_text_button = tk.Button(frame_alt, text="metin oku (erkek)",command=self.oku_f)
        self.read_text_button.pack()"""
        self.gender_combobox = ttk.Combobox(frame_alt, values=["erkek","kadın","çocuk","yaşlı erkek","yaşlı kadın"])
        self.gender_combobox.pack(pady=5)

        self.read_text_button = tk.Button(frame_alt, text="metin oku ",command=self.metni_oku)
        self.read_text_button.pack(padx=3)
        

        self.ip_scan_button = Button(frame_sol, text="IP TARA",command= self.scan_ip)
        self.ip_scan_button.pack()

        self.connect_button = tk.Button(frame_sol, text="Bağlan",command=self.connect_to_server)
        self.connect_button.pack(padx=3)

        self.start_button = tk.Button(frame_orta, text="Başlat",cursor="hand2",command=self.start_communication, state="disabled")
        self.start_button.pack(side=TOP, pady=5)

        self.stop_button = tk.Button(frame_orta, text="stop",cursor="hand2",command=self.stop_communication, state="disabled" )
        self.stop_button.pack()

        self.get_sound_button = tk.Button(frame_orta, text="Ses Al",cursor="hand2",command=self.get_sound, state="disabled" )
        self.get_sound_button.pack(side=TOP,padx=10, pady=5)

        self.get_sound_contunie_button = tk.Button(frame_orta, text="Ses Alı Devam Et",cursor="hand2",command=self.get_sound_continue, state="disabled")
        self.get_sound_contunie_button.pack()  
        
        self.get_sound_stop_button = tk.Button(frame_orta, text="Ses Alı Duraklat",cursor="hand2",command=self.get_sound_stop, state="disabled" )
        self.get_sound_stop_button.pack(side=TOP,padx=10, pady=5)

        self.disconnect_button = tk.Button(frame_orta, text="Bağlantıyı kes",cursor="hand2",command=self.disconnect, state="disabled")
        self.disconnect_button.pack()
        self.scan_ip()
        self.root.mainloop()    


    def read_text(self):
        selected_gender = self.gender_combobox.get()
        if selected_gender =="erkek":
            self.read_man_thread()

        elif selected_gender =="kadın":
            self.read_text__woman_thread()

        elif selected_gender == "yaşlı erkek":
            self.read__old_man_t()
            
        elif selected_gender == "yaşlı kadın":
            self.read__old_woman_t()
        elif selected_gender == "çocuk":
            self.read_children_thread()

    def receive_text(self):
           
           
        server_socket_text = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket_text.connect((self.HOST, self.PORT_TEXT))
       # self.server_socket,adress = se
        print(f"Metin için Bağlantı sağlandı: {self.HOST}")
        while True:
            try:
                data = server_socket_text.recv(1024)
                

                # Check the data type based on the flag
                
                metin = data.decode("utf-8")
                self.metin_yeri.insert(tk.END, metin + "\n")
                self.metin_yeri.see(tk.END)  # Scrollbar ile otomatik olarak en sona inmesini sağlar
                self.root.update()  # GUI'yi güncellemek için root penceresini yeniler


            except ConnectionResetError:
                break
        server_socket_text.close()

    def receive_text_thread(self):
        ti1 = threading.Thread(target=self.receive_text)
        ti1.start()

    def read_woman(self,metin):
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.FEMALE, rate=0.47, pitch=0.5, vol=1)
        self.metin_yeri.delete("1.0", tk.END)
        self.is_reading = False  
        
    def read_text__woman_thread(self):
        
            if not self.is_reading:
                self.is_reading = True
                metin = self.metin_yeri.get("1.0", tk.END)
                threading.Thread(target=self.read_woman, args=(metin,)).start()



    def read_man_thread(self):
        if not self.is_reading:
            self.is_reading = True
            metin = self.metin_yeri.get("1.0", tk.END)
            threading.Thread(target=self.read_man, args=(metin,)).start()

    def read_man(self, metin):
        
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.MALE, rate=0.47, pitch=0.36, vol=1)
        self.metin_yeri.delete("1.0", tk.END)
        self.is_reading = False



    def read_old_man(self,metin):
        
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.MALE, rate=0.33, pitch=0.25, vol=1)
        self.metin_yeri.delete("1.0", tk.END)
        self.is_reading = False

    
    def read__old_man_t(self):
        if not self.is_reading:
            self.is_reading = True
            metin = self.metin_yeri.get("1.0", tk.END)
            threading.Thread(target=self.read_old_man, args=(metin,)).start()


    def read_old_woman(self,metin):
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.FEMALE, rate=0.36, pitch=0.28, vol=1)
        self.metin_yeri.delete("1.0", tk.END)
        self.is_reading = False

    def read__old_woman_t(self):
        if not self.is_reading:
            self.is_reading = True
            metin = self.metin_yeri.get("1.0", tk.END)
            threading.Thread(target=self.read_old_woman, args=(metin,)).start()

    def read_children(self,metin):
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.FEMALE, rate=0.45, pitch=0.75, vol=0.5)
        self.metin_yeri.delete("1.0", tk.END)
        self.is_reading = False  
        
    def read_children_thread(self):
        
            if not self.is_reading:
                self.is_reading = True
                metin = self.metin_yeri.get("1.0", tk.END)
                threading.Thread(target=self.read_children, args=(metin,)).start()
            


    def scan_ip(self):
        nm = nmap.PortScanner()
        nm.scan('192.168.1.0/24', arguments='-sn')
        hosts = nm.all_hosts()

        print("Ağdaki tüm cihazların IP ve MAC adresleri:")
        for host in hosts:
            if 'mac' in nm[host]['addresses']:
                ip_address = nm[host]['addresses']['ipv4']
                mac_address = nm[host]['addresses']['mac']
                self.listbox.insert(tk.END,ip_address+"     "+str(mac_address))
                #print(ip_address, mac_address)


    def handle_listbox_double_click(self, event):
        selected_item = self.listbox.get(tk.ACTIVE)
        selected_ip = selected_item.split()[0]  # Sadece IP adresini combobox'a gönder
        self.ip_combobox.set(selected_ip)

    def connect_to_server(self):
        selected_ip = self.ip_combobox.get()
        self.HOST = selected_ip

        if selected_ip not in self.get_saved_ip_addresses():
            self.save_ip_address(selected_ip)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.HOST, self.PORT))
        print(f"Bağlantı sağlandı: {self.HOST}")
        self.receive_text_thread()



        self.start_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.get_sound_button.config(state="normal")
        self.disconnect_button.config(state="normal")
        #self.metin_al_f.config(state="normal")


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
        

        stream.stop_stream()
        stream.close()
        speaker_stream.stop_stream()
        speaker_stream.close()
        p.terminate()

        
        #self.server_socket.close()

    def disconnect(self):
        self.is_running = False  # Gönderim ve ses alma işlemlerini durdur
        self.is_running_recv = False
        self.contunie = False

        if self.server_socket is not None:
            try:

                self.server_socket.shutdown(socket.SHUT_RDWR)   
                self.server_socket.close()
            except (OSError,AttributeError):
                print("gg")
                pass
        self.root.quit()

    def start_communication(self):
        if not self.is_running:
            self.is_running = True
            threading.Thread(target=self.send_audio).start()

    def get_sound(self):
        self.is_running_recv = True
        threading.Thread(target=self.receive_audio).start()
        #self.get_sound_button.config(state="disabled")
        self.get_sound_contunie_button.config(state="normal")

    def get_sound_stop(self):
        self.event.clear()
        self.get_sound_stop_button.config(state="disabled")
        self.get_sound_contunie_button.config(state="normal")

    def get_sound_continue(self):
        self.event.set()
        self.get_sound_contunie_button.config(state="disabled")
        self.get_sound_stop_button.config(state="normal")

    def stop_communication(self):
        if self.is_running:
            self.is_running = False

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
                audio_data = np.frombuffer(data, np.int16)
                self.server_socket.sendall(audio_data)

                if not self.is_running:
                    return
            except Exception as e:
                if self.server_socket is not None and self.contunie ==True:

                    print("Beklenmedik bir hata oluştu... Lütfen bekleyiniz: ", e)
                    print("Yeniden bağlanılmaya çalışılıyor.")
                    self.connect_to_server()
               

                """data = stream.read(self.CHUNK)
                audio_data = np.frombuffer(data, np.int16)
                self.server_socket.sendall(audio_data)

                if not self.is_running:
                    break"""

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
            try:
                data = self.server_socket.recv(self.CHUNK)

                if not data:
                    break

                if self.event.is_set() and self.contunie:
                    stream.write(data)
            except Exception as e:
                if self.server_socket is not None and self.contunie:
                    print("Bağlantı sıfırlandı... Yeniden bağlanılıyor.\n", e)
                    self.connect_to_server()
                    
                    data = self.server_socket.recv(self.CHUNK)

                    if not data:
                        break

                    if self.event.is_set() and self.contunie:
                        stream.write(data)
                    

        stream.stop_stream()
        stream.close()
        self.server_socket.close()
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
