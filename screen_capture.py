import os
import time
from datetime import datetime

def capture_screen():
    """Funkcja do robienia zrzutów ekranu"""
    try:
        # Sprawdź czy mamy dostęp do systemowych narzędzi
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        
        # Dla różnych systemów
        if os.name == 'posix':  # Linux/Mac/Android (Termux)
            # Wymaga termux-api
            os.system(f"termux-screenshot {filename}")
        elif os.name == 'nt':  # Windows
            # Możesz użyć PIL do zrzutu ekranu
            pass
        
        return filename
    except Exception as e:
        print(f"Błąd podczas robienia zrzutu: {e}")
        return None

def get_screenshots_dir():
    """Zwraca katalog z zrzutami"""
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    return screenshots_dir
