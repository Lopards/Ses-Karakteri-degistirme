import tkinter as tk
from gtts import gTTS
from playsound import playsound



def metin():
    def kaydet_oku():
        text = text_entry.get("1.0", tk.END).strip()  # metni al
        if text:
           
            language = 'tr'  
            speech = gTTS(text=text, lang=language, slow=False)
            speech.save("metin_Sesi.wav")
            
            playsound("metin_Sesi.wav")

    # tkinter ile arayüz
    window = tk.Tk()
    window.title("Metin Okuma")

    text_entry = tk.Text(window, height=10, width=50)
    text_entry.pack()

   
    save_button = tk.Button(window, text="Kaydet ve Oku", command=kaydet_oku)
    save_button.pack()

    
    window.mainloop() 
