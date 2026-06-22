import serial

esp = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def lcd(text):
    try:
        message = f"LCD:{text}\n"
        esp.write(message.encode())

    except Exception as e:
        print(f"Failed to update LCD: {e}")