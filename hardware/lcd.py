# hardware/LCD.py

class LCD:
    def __init__(self, esp32):
        self.esp32 = esp32

    def show(self, text):
        self.esp32.send_lcd(text)