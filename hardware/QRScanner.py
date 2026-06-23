import cv2
import json
from hardware.lcd import lcd
from config import QR_CAMERA_PATH

class QRScanner:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

        # Force Suyin HD Camera (stable device ID)
        self.camera_path = QR_CAMERA_PATH

    def scan(self):
        cap = cv2.VideoCapture(self.camera_path, cv2.CAP_V4L2)

        if not cap.isOpened():
            print("Cannot open Suyin HD Camera")
            return None

        # Improve performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
                    cv2.destroyAllWindows()
                    return payload

                except Exception as e:
                    print(f"Error decoding QR data: {e}")
                    lcd("Invalid QR Code")

            cv2.imshow("QR Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return None