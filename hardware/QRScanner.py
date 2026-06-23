# hardware/QRScanner.py
import cv2
import json
from hardware.lcd import lcd
from config import QR_CAMERA_PATH

class QRScanner:
    def __init__(self, qr_camera_path=QR_CAMERA_PATH):
        self.cam_path = qr_camera_path
        self.detector = cv2.QRCodeDetector()

    def scan(self):
        cap = cv2.VideoCapture(self.cam_path, cv2.CAP_V4L2)  # Use V4L2 backend for Linux
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
        