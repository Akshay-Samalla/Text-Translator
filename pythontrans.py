import os
import tkinter as tk 
from tkinter import ttk 
from googletrans import Translator 
from gtts import gTTS 
import pygame 
from PIL import ImageTk, Image 

class TranslationApp: 
    def __init__(self, root):
        self.root = root 
        self.root.title("Translator")
        
        # Initialize Pygame mixer
        pygame.mixer.init()

        background_image = Image.open(r"./wooden-stairs-pink-2560x1080-15788.jpg") 
        self.background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(root, image=self.background_photo)
        background_label.place(relwidth=1 , relheight=1)
        root.config(bg="#ffffff")
        style = ttk.Style()
        style.configure("TLabel", background="#ffffff", font=("Helvetica", 12))
        style.configure("TButton", background="#000000", foreground="#000000", font=("Helvetica", 12))
        style.configure("TCombobox", background="#ffffff", font=("Helvetica", 12))
        input_frame = tk.Frame(root, bg="#ffffff", bd=5)
        input_frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.1, anchor="n")

        self.text_entry = ttk.Entry(input_frame, width=50)
        self.text_entry.place(relwidth=0.7, relheight=1)

        self.translate_button = ttk.Button(input_frame, text="Translate", command=self.translate_text)
        self.translate_button.place(relx=0.7, relheight=1, relwidth=0.3)

        
        lang_frame = tk.Frame(root, bg="#ffffff", bd=5)
        lang_frame.place(relx=0.5, rely=0.25, relwidth=0.8, relheight=0.1, anchor="n")

        self.label2 = ttk.Label(lang_frame, text="Select Source Language:")
        self.label2.place(relx=0, relheight=1)

        self.src_lang_combo = ttk.Combobox(lang_frame, values=["English", "French" ,"Italian", "Russian", "Japanese", "Arabic", "Hindi"])
        self.src_lang_combo.place(relx=0.3, relheight=1)

        self.label3 = ttk.Label(lang_frame, text="Select Destination Language:")
        self.label3.place(relx=0.5, relheight=1)

        self.dest_lang_combo = ttk.Combobox(lang_frame, values=["English", "French",  "Italian", "Russian", "Japanese", "Arabic", "Hindi"])
        self.dest_lang_combo.place(relx=0.8, relheight=1)

       
        self.update_combobox_widths()

        self.src_lang_combo.set("English")
        self.dest_lang_combo.set("French")

        
        output_frame = tk.Frame(root, bg="#ffffff", bd=5)
        output_frame.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.3, anchor="n")

        self.translated_text = tk.Text(output_frame, wrap="word")
        self.translated_text.place(relwidth=1, relheight=1)

      
        self.pronounce_button = ttk.Button(root, text="Pronounce", command=self.pronounce_text)
        self.pronounce_button.place(relx=0.5, rely=0.75, relwidth=0.3, relheight=0.1, anchor="n")

    def update_combobox_widths(self):
        src_lang_max_width = max([len(lang) for lang in self.src_lang_combo["values"]])
        dest_lang_max_width = max([len(lang) for lang in self.dest_lang_combo["values"]])

        self.src_lang_combo.config(width=src_lang_max_width + 2)  
        self.dest_lang_combo.config(width=dest_lang_max_width + 2)  

    def translate_text(self):
        dest_lang = self.dest_lang_combo.get().lower()
        print("Destination language:", dest_lang)
        translator = Translator()
        translated = translator.translate(
            self.text_entry.get(),
            src=self.src_lang_combo.get().lower(),
            dest=dest_lang
        )
        self.translated_text.delete(1.0, tk.END)
        self.translated_text.insert(tk.END, translated.text)

    def pronounce_text(self):
        text_to_pronounce = self.translated_text.get(1.0, tk.END).strip()
        if text_to_pronounce:
            lang_code = self.dest_lang_combo.get().lower()[:2] 
            supported_lang_codes = ["en", "fr", "es", "de", "it", "ru", "zh", "ja", "ar", "hi"]
            if lang_code not in supported_lang_codes:
                print("Unsupported language code:", lang_code)
                return
            tts = gTTS(text=text_to_pronounce, lang=lang_code)
            if os.path.exists("pronunciation.mp3"):
                pygame.mixer.stop()  
                pygame.mixer.quit()  
                while pygame.mixer.get_busy(): 
                    pass
                os.remove("pronunciation.mp3") 
            tts.save("pronunciation.mp3")
            pygame.mixer.init()
            pygame.mixer.music.load("pronunciation.mp3")
            pygame.mixer.music.play()
        else:
            print("No text available for pronunciation.")
   
def main():
    root = tk.Tk()
    app = TranslationApp(root)
    root.geometry("1000x900")  
    root.mainloop()

if __name__ == "__main__":
    main()
