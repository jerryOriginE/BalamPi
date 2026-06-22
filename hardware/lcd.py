import requests
from config import ESP32_IP

def lcd(text):
    try:
        requests.get(
            f"http://{ESP32_IP}/lcd",
            params={"text": text},
            timeout=2
        )

    except Exception as e:
        print(f"Failed to update LCD: {e}")