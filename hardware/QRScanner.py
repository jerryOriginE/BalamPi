import cv2
import json
from hardware.lcd import lcd
from config import CAMERA_INDEX

class QRScanner:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def scan(self):
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            print("Cannot open camera")
            return None
        
        start = cv2.getTickCount()
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            data, points, _ = self.detector.detectAndDecode(frame)

            if data:
                try:
                    payload = json.loads(data)
                    lcd("QR Code Detected")

                    cap.release()
                    return payload
                
                except Exception as e:
                    print(f"Error decoding QR data: {e}")
                    lcd("Invalid QR Code")
                    continue

            cv2.imshow("QR Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return None
        