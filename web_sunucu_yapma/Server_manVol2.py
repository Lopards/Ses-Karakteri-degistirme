import speech_recognition as sr
from tkinter import *
import tkinter as tk
import threading
import requests
import socket
import pyaudio
import numpy as np
import threading
import tkinter as tk
import tkinter.ttk as ttk
from scipy import signal 
from urllib import request
import speech_recognition as sr
import time
import sys
import make_a_server
from http.server import BaseHTTPRequestHandler, HTTPServer
#from web_sunucu_yapma.make_a_server import ServerApp

# server_man.py denemesidir.

class SesIletisimArayuzuE:
    def __init__(self):
        self.HOST = None
        self.PORT = 12345
        self.PORT_TEXT =12346
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 22050
        self.PITCH_SHIFT_FACTOR = 1.2

        self.event = threading.Event()
        self.contunie = True
        self.flag = None
        self.metin_flag = False
        self.internet_baglantisi = False
        self.client_socket_text = None
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
        self.root.geometry("1000x400")

        
        frame_ustbolge = Frame(self.root, bg="#0080FF")
        frame_ustbolge.place(relx=0.03, rely=0.1, relwidth=0.75, relheight=0.1)

        frame_altSol = Frame(self.root, bg="#0080FF")
        frame_altSol.place(relx=0.03, rely=0.21, relwidth=0.36, relheight=0.66)

        frame_altSag = Frame(self.root, bg="#0080FF")
        frame_altSag.place(relx=0.40, rely=0.21, relwidth=0.38, relheight=0.66)

        self.frame_deep = Frame(self.root)
        self.frame_deep.place(relx=0.79, rely=0.21, relwidth=0.22, relheight=0.66)

        self.ip_combobox = ttk.Combobox(frame_ustbolge, values=self.get_saved_ip_addresses())
        self.ip_combobox.pack(padx=10,side=LEFT)

        self.ip_scan_button = tk.Button(frame_ustbolge, text="ip tara",cursor="hand2", command=self.get_local_ip)
        self.ip_scan_button.pack(side=LEFT,pady=3)

        self.connect_button = tk.Button(frame_ustbolge, text="Bağlan",cursor="hand2", command=self.connect_to_server)
        self.connect_button.pack(side=LEFT,pady=3,padx=5)

        self.start_button = tk.Button(frame_altSol, text="Başlat",cursor="hand2", command=self.start)
        self.start_button.pack(side=TOP, pady=5)

        self.stop_button = tk.Button(frame_altSol, text="stop",cursor="hand2", command=self.stop)
        self.stop_button.pack()

        self.get_sound_button = tk.Button(frame_altSol, text="Ses Al",cursor="hand2", command=self.start_get_sound,disabledforeground="#a9a9a9")
        self.get_sound_button.pack(side=TOP,padx=10, pady=5)

        self.get_sound_contunie_button = tk.Button(frame_altSol, text="Ses Alı Devam Et",cursor="hand2", command=self.get_sound_contunie)
        self.get_sound_contunie_button.pack()  
        
        self.get_sound_stop_button = tk.Button(frame_altSol, text="Ses Alı Duraklat",cursor="hand2", command=self.get_sound_stop)
        self.get_sound_stop_button.pack(side=TOP,padx=10, pady=5)

        self.disconnect_button = tk.Button(frame_altSol, text="Bağlantıyı kes",cursor="hand2", command=self.disconnect)
        self.disconnect_button.pack()

        self.text_place = tk.Text(frame_altSag,height=10,width=33)
        self.text_place.pack()

        self.speech_to_text_button = tk.Button(frame_altSag, text="sesi yazıya dök",cursor="hand2", command=self.baslat_text)
        self.speech_to_text_button.pack(pady=5)

        self.stop_speech_to_text_button = tk.Button(frame_altSag, text="durdur",cursor="hand2", command=self.stop_speech_to_text)
        self.stop_speech_to_text_button.pack()


        self.text_send_button = tk.Button(frame_altSag, text="yazıyı gönder",cursor="hand2", command=self.yazi_gonder_t)
        self.text_send_button.pack(pady=5)

        self.text_web = tk.Button(frame_altSag, text="sunucu gönder",cursor="hand2", command=self.web)
        self.text_web.pack(pady=5)

        self.root.bind("<KeyPress>", self.klavye_kontrol)
        self.root.bind("<KeyRelease>", self.klavye_kontrol)
        
        
        p = pyaudio.PyAudio()
        self.stream = None
        self.stop_event = threading.Event()

        

        self.output_device_list = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                device_name = device_info["name"]
                self.output_device_list.append((i, device_name))
                if len(self.output_device_list) == 6:
                    break
        self.output_device_list = tuple(self.output_device_list)
        
        self.output_device_label = tk.Label(self.frame_deep, text="Ses Çıkışı:")
        self.output_device_label.pack()

        self.output_device_listbox = tk.Listbox(self.frame_deep, selectmode=tk.SINGLE,height=13,width=30)
        self.output_device_listbox.pack(side="top")
        
        for device in self.output_device_list:
            self.output_device_listbox.insert(tk.END, device[1])

        self.select_button = tk.Button(self.frame_deep, text="Seç", command=self.play_button_clicked,cursor="hand2",activeforeground="red")
        self.select_button.pack()

        
        self.get_local_ip()
        self.root.mainloop()
        
        
        
                            ##### ********** ######
    def web(self):
        
        make_a_server.ServerApp()
        if make_a_server.ServerApp:
            make_a_server.mesaj = self.text_place.get("1.0",tk.END)
            self.text_place.delete("1.0",tk.END)
            
        
      


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
        self.yazi_gonder_t()
        
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
        #self.server_socket.close()

    def disconnect(self):
            
        self.is_running = False  # Gönderim ve ses alma işlemlerini durdur
        self.is_running_recv = False
        self.contunie = False
        
        if self.client_socket is not None:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except (OSError, AttributeError):
                pass
           
        
        if self.server_socket is not None:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
            except (OSError, AttributeError):
                pass
            
        
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
        
        Esik_deger = 10
        
        while self.is_running:
            self.connect()
            
            
            data = stream.read(self.CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            if np.abs(audio_data).mean() > Esik_deger: # mikrofona gelen ses verilerin MUTLAK değerinin ortalamasını alarak ses şiddetini buluyoruz. ortalama, eşik değerinden yüksekse ses iletim devam ediyor.
                mikrofon = True
                
            else:
                mikrofon  = False
                
            
            
            try:
                    if self.is_running and mikrofon:
                    
                        converted_data = signal.resample(audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR)) * 1.4
                        converted_data = converted_data.astype(np.int16)
                        converted_data_bytes = converted_data.tobytes()
                        self.client_socket.sendall(converted_data_bytes)

                    if not self.is_running:
                            return
          
            
            except Exception as e:
                    if self.client_socket is not None and self.contunie == True:
                        print("bir hata oldu : ",e)
                        print("yeniden bağlanılmaya çalışılıyor...")
                        self.client_socket.close()
                        self.client_socket, address = self.server_socket.accept()
                        print(f"* {address} adresinden yeni bir bağlantı alındı.")
        

         
                    


        
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
            # İnternet bağlantısını kontrol et
            check_net = self.connect()
            if not check_net:
                # Eğer bağlantı yoksa uygun uyarıyı ver ve bir süre bekle
                print("İnternet bağlantısı yok! Uyarı: Bağlantı kopmuş olabilir.")
                time.sleep(3)
                continue

            try:
                data = self.client_socket.recv(self.CHUNK)
                if not data:
                    break
                if self.event.is_set() and self.contunie:
                    self.play_server_output(data)
                else:
                    print("Ses al devam tuşuna bas")
            except Exception as e:
                if self.client_socket is not None and self.contunie:
                    print("Beklenmeyen bir hata oluştu:", e)
                    print("Yeni bir bağlantı bekleniyor...")
                    self.client_socket.close()
                    self.client_socket, address = self.server_socket.accept()
                    print(f"* {address} adresinden yeni bir bağlantı alındı.")
            

        stream.stop_stream()
        stream.close()
        self.client_socket.close()
        p.terminate()
        
        

                
            
        
                    

    def get_local_ip(self):
        
            #  local IP adresini alıyoruz
            local_ip = socket.gethostbyname(socket.gethostname())
            self.ip_combobox.insert(tk.END,local_ip)
            
                
    

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
        if  self.is_running !=True:
            self.is_running = True
            threading.Thread(target=self.send_audio).start()
                            ##### ********** ######
    def stop(self):
        
            self.is_running = False
            

                            ##### ********** ######
    def klavye_kontrol(self, event):
        if event.char == 'q':
            if event.type == tk.EventType.KeyPress:
                self.contunie = True
            elif event.type == tk.EventType.KeyRelease:
                self.contunie = False

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
        

        while True:
            try:
                # www.google.com adresine bağlanmayı dene (80 ve 443 portları genellikle açıktır)
                socket.gethostbyname("www.google.com")
                if not self.internet_baglantisi:
                    print("İnternet bağlantısı aktif.")
                    self.internet_baglantisi = True
                return True
            except socket.gaierror:
                if self.internet_baglantisi:
                    print("İnternet bağlantısı yok! Uyarı: Bağlantı kopmuş olabilir.")
                    self.internet_baglantisi = False
                return False


    def sesi_anlik_yaziya_cevir(self):
        while self.flag:

            
            r = sr.Recognizer()

            with sr.Microphone() as source:
                print("Dinleme başladı. Konuşun...")

                while self.flag:

                    audio = r.listen(source)

                    try:
                            text = r.recognize_google(audio, language="tr-TR")
                            if text:
                                
                                self.text_place.insert(tk.END,text+str(". "))
                    except sr.UnknownValueError:
                            print("Ses anlaşılamadı.")
                    except sr.RequestError as e:
                            print("İstek başarısız oldu; {0}".format(e))

        print("mikrofon kapandı.")

    def baslat_text(self):
        
            self.flag = True
            threading.Thread(target=self.sesi_anlik_yaziya_cevir).start()
        

    def stop_speech_to_text(self):
        #sei yazıya dökme durdur
        self.flag = False
    
    def yazi_gonder(self):
        
            try:
                if not self.metin_flag:
                    server_socket_text = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket_text.bind((self.HOST, self.PORT_TEXT))
                    server_socket_text.listen(1)           
                    print(f"* Metin için {self.HOST}:{self.PORT_TEXT} dinleniyor...")

                    self.client_socket_text, address = server_socket_text.accept()
                    print(f"* Metin için {address} bağlanıldı.")

                    self.metin_flag = True  # Bayrağı True olarak ayarla, böylece tekrardan bağlantı kurmuyor

                metin = self.text_place.get("1.0", tk.END).strip()

                if metin:
                    # Metin verisini ikinci soket üzerinden gönder
                    self.client_socket_text.send(bytes(metin, "utf-8"))
                    self.text_place.delete("1.0", tk.END)
                    print("Metin gönderildi:", metin)
            except Exception as e:
                print("metin gönderme işlemi duraklatıldı...", e)
                # Bağlantı hatası oluştuğunda, tekrar bağlantı kurmak için bayrağı False yap
                self.metin_flag = False
                # Socketi kapat ve yeniden bağlantıyı kurmak için çağrı yap
                if self.client_socket_text:
                    self.client_socket_text.close()
        

        


    def yazi_gonder_t(self):
        """if not self.metin_flag:
            self.metin_flag = True"""
        t1 = threading.Thread(target=self.yazi_gonder)
        t1.start()
        

                            ##### ********** ######
    """def stop_button_clicked(self):
        self.stop_event.set()"""

    
                                     ##### ********** ######   


if __name__ == "__main__":
    ses_arayuzu = SesIletisimArayuzuE()
