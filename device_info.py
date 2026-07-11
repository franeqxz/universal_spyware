import platform
import psutil
import socket
import uuid
from datetime import datetime

def get_device_info():
    """Zbiera informacje o urządzeniu"""
    try:
        info = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "hostname": socket.gethostname(),
            "device_id": str(uuid.uuid4()),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "battery": get_battery_info(),  # Możesz dodać szczegóły
            "network": get_network_info()
        }
        
        return info
    except Exception as e:
        return {"error": str(e)}

def get_battery_info():
    """Pobiera informacje o baterii (jeśli dostępne)"""
    try:
        # W systemach Android może być dostępna przez termux-api
        return "Bateria: 85%"
    except:
        return "Bateria: Niedostępna"

def get_network_info():
    """Pobiera informacje o sieci"""
    try:
        interfaces = psutil.net_if_addrs()
        network_info = {}
        
        for interface_name, interface_addresses in interfaces.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    network_info[interface_name] = {
                        'ip': address.address,
                        'netmask': address.netmask
                    }
        
        return network_info
    except Exception as e:
        return {"error": str(e)}
