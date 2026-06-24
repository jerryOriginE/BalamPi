import cv2
import json
import os
import re
from config import QR_CAMERA_PATH

class QRScanner:
    def __init__(self, qr_camera_path=QR_CAMERA_PATH, lcd=None):
        self.cam_path = qr_camera_path
        self.detector = cv2.QRCodeDetector()
        self.lcd = lcd

    def scan(self):
        # Resolve the symlink to a real path (e.g., /dev/videoX)
        real_path = os.path.realpath(self.cam_path)
        match = re.search(r'(\d+)$', real_path)
        camera_index = None
        if match:
            camera_index = int(match.group(1))
            print(f"Resolved camera index: {camera_index} from path: {real_path}")
        else:
            print(f"Could not resolve camera index from path: {real_path}")
            return None

        cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2) 
        
        if not cap.isOpened():
            print(f"Cannot open camera at index {camera_index}")
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
                    if self.lcd: self.lcd.show("QR Code Detected") # Guard if lcd is None

                    cap.release()
                    return payload
                
                except Exception as e:
                    print(f"Error decoding QR data: {e}")
                    if self.lcd: self.lcd.show("Invalid QR Code")
                    continue

            cv2.imshow("QR Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return None