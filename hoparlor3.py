import pyaudio
import tkinter as tk
import threading



class SesOynatici:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.stop_event = threading.Event()

        self.root = tk.Tk()
        self.root.title("Mikrofon Çıkışı Değiştirici")

        self.output_device_list = []
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                device_name = device_info["name"]
                self.output_device_list.append((i, device_name))
                if len(self.output_device_list) == 5:
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

    def set_output_stream(self, output_device,ses):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024

        self.output_stream = self.p.open(
            output=True,
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            frames_per_buffer=self.chunk,
            output_device_index=output_device,
        )

    def play_server_output(self, data):
        self.output_stream.write(data)

    def select_output_device(self):
        device_index = self.output_device_listbox.curselection()
        output_device = self.output_device_list[device_index[0]][0]
        return output_device

    def play_button_clicked(self, data):
        output_device = self.select_output_device()
        self.stop_event.clear()
        self.set_output_stream(output_device)
        self.play_server_output(data)

    def stop_button_clicked(self):
        self.stop_event.set()

    def run(self):
        self.root.mainloop()
        

if __name__ =="__main__":
    ses = SesOynatici()
    ses.run()
