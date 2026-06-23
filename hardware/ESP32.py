# hardwware/ESP32.py
import serial
import threading

class ESP32:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.serial = serial.Serial(
            port,
            baudrate,
            timeout=1
        )

        self.button_callback = None

    def send_lcd(self, text):
        try:
            self.serial.write(
                f"LCD:{text}\n".encode()
            )

        except Exception as e:
            print(f"Error sending to ESP32: {e}")

    def on_button(self, callback):
        self.button_callback = callback

    def start(self):
        threading.Thread(
            target=self._listen,
            daemon=True
        ).start()

    def _listen(self):
        while True:
            try:
                line = self.serial.readline().decode().strip()

                if line == "BUTTON":
                    if self.button_callback:
                        self.button_callback()

            except Exception as e:
                print(f"Error reading from ESP32: {e}")