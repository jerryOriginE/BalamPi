from config import *

from hardware.ESP32 import ESP32
from hardware.LCD import LCD
from hardware.QRScanner import QRScanner

from auth.SessionManager import SessionManager
from auth.AuthService import AuthService

from backend.APIClient import APIClient

from ai.WasteAI import WasteAI

from recycling.CooldownManager import CooldownManager
from recycling.RecyclingProcessor import RecyclingProcessor

from core.SystemController import SystemController

from ars.ARS import ARS

def build_system():
    esp = ESP32(port=ESP32_PORT, baudrate=ESP32_BAUDRATE)
    lcd = LCD(esp)
    scanner = QRScanner(qr_camera_path=QR_CAMERA_PATH, lcd=lcd)

    api = APIClient(BACKEND_URL)

    session = SessionManager()

    auth = AuthService(scanner, api)

    ai = WasteAI(
        model_path=AI_MODEL_PATH,
        camera_index=WASTE_CAMERA_PATH,
        confidence_threshold=CONFIDENCE_THRESHOLD,
        stable_frames=STABLE_FRAMES,
        lcd=lcd
    )

    ars = ARS(lcd=lcd)
    ars.calibrate()

    cooldown = CooldownManager(DETECTION_COOLDOWN)

    processor = RecyclingProcessor(
        ars=ars,
        api=api,
        session=session,
        lcd=lcd,
        cooldown=cooldown
    )

    controller = SystemController(
        esp32=esp,
        lcd=lcd,
        auth=auth,
        api=api,
        session=session,
        ai=ai,
        processor=processor
    )

    return controller

def main():
    controller = build_system()
    controller.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down...")
        
if __name__ == "__main__":
    main()