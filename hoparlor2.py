import pyaudio
import tkinter as tk
import threading


class SesOynatici:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None  # stream değişkeni tanımlandı
        self.stop_event = threading.Event()  # durdurma olayı oluşturuldu

        self.root = tk.Tk()
        self.root.title("Mikrofon Çıkışı Değiştirici")

        self.output_device_list = []
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                device_name = device_info["name"]
                self.output_device_list.append((i, device_name))
                if len(self.output_device_list) ==5:
                    break
        self.output_device_list = tuple(self.output_device_list)

        self.output_device_label = tk.Label(self.root, text="Ses Çıkışı:")
        self.output_device_label.pack()

        self.output_device_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.output_device_listbox.pack()
        for device in self.output_device_list:
            self.output_device_listbox.insert(tk.END, device[1])

        self.select_button = tk.Button(self.root, text="Seç", command=self.play_button_clicked)
        self.select_button.pack()

        self.stop_button = tk.Button(self.root, text="Durdur", command=self.stop_button_clicked)
        self.stop_button.pack()

    def play_microphone_output(self, output_device):
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 44100
        p = pyaudio.PyAudio()
        stream = p.open(input=True,
                                  output_device_index=output_device,
                                  format=format,
                                  channels=channels,
                                  rate=rate,
                                  frames_per_buffer=chunk)

        output_stream = p.open(output=True,
                                    format=format,
                                    channels=channels,
                                    rate=rate,
                                    frames_per_buffer=chunk,
                                    output_device_index=output_device)

        while not self.stop_event.is_set():  # durdurma olayı kontrol ediliyor
            data = stream.read(chunk)
            output_stream.write(data)

        stream.stop_stream()
        stream.close()
        output_stream.stop_stream()
        output_stream.close()

    def select_output_device(self):
        device_index = self.output_device_listbox.curselection()
        output_device = self.output_device_list[device_index[0]][0]
        return output_device

    def play_button_clicked(self):
        output_device = self.select_output_device()
        self.stop_event.clear()  # durdurma olayı sıfırlanıyor
        play_thread = threading.Thread(target=self.play_microphone_output, args=(output_device,))
        play_thread.start()

    def stop_button_clicked(self):
        self.stop_event.set()  # durdurma olayı ayarlanıyor

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ses_oynatici = SesOynatici()
    ses_oynatici.run()
