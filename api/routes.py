import threading
import serial
import requests

from hardware.lcd import lcd
from hardware.QRScanner import QRScanner
from config import BACKEND_URL


def setup_routes(app, ai, session):

    # ESP32 SERIAL CONNECTION
    esp = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    scanner = QRScanner()

    print("ESP32 serial connected")

    # LCD helper (ESP32 via USB)
    def lcd_msg(text):
        try:
            esp.write(f"LCD:{text}\n".encode())
        except Exception as e:
            print(f"LCD error: {e}")

    # CORE BUTTON HANDLER
    def handle_button():
        print("Button Pressed")

        lcd_msg("Scanning QR...")

        qr_data = scanner.scan()

        if qr_data is None:
            lcd_msg("No QR detected")
            return

        print(f"QR Data: {qr_data}")
        lcd_msg("Verifying...")

        try:
            response = requests.post(
                BACKEND_URL + "/auth/verify-user",
                json=qr_data,
                timeout=5
            )

            result = response.json()
            print(f"Verification Result: {result}")

        except Exception as e:
            print(f"Error verifying user: {e}")
            lcd_msg("Verification Failed")
            return

        # SUCCESS / FAIL LOGIC
        if result.get("valid"):
            user = result["user"]

            print(f"User {user['name']} verified successfully")

            lcd_msg(f"Welcome {user['name']}")

            session.start(user)
            ai.start()

        else:
            lcd_msg("Access Denied")

    # SERIAL LISTENER THREAD
    def serial_listener():
        while True:
            try:
                line = esp.readline().decode(errors='ignore').strip()

                if not line:
                    continue

                print(f"[ESP32] {line}")

                if line == "BUTTON":
                    handle_button()

            except Exception as e:
                print(f"Serial error: {e}")

    threading.Thread(target=serial_listener, daemon=True).start()

    @app.get("/")
    def home():
        return {"message": "ARS Online (USB Serial Mode)"}