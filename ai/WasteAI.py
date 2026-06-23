from ultralytics import YOLO
import cv2
import time
import threading
from config import AI_MODEL, AI_CAMERA_PATH, AI_TIMEOUT, CONFIDENCE_THRESHOLD

class WasteAI:
    def __init__(self, ars, session):
        self.ars = ars
        self.session = session

        self.model = YOLO(AI_MODEL)

        self.active = False
        self.busy = False

        self.cap = None

        self.last_lalbel = None
        self.counter = 0

        self.lock = threading.Lock()
        self.last_process_time = 0

    def start(self):
        with self.lock:
            print("Starting AI...", self.active)
            
            if self.active:
                return

            self.active = True

            if self.cap:
                self.cap.release()

            self.cap = cv2.VideoCapture(AI_CAMERA_PATH, cv2.CAP_V4L2)
            time.sleep(0.5) # warmup cam
            print("AI  Started")

    def stop(self):
        with self.lock:
            self.active = False
        
        if self.cap:
            self.cap.release()
            self.cap = None

        print("AI Stopped")

    def run_background(self):
        thread = threading.Thread(
            target=self.loop,
            daemon=True
        )

        thread.start()

    def loop(self):
        while True:
            try: 
                if not self.active or self.cap is None:
                    time.sleep(0.1)
                    continue
    
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    continue
    
                if self.cap is None:
                    time.sleep(0.1)
                    continue
    
                result = self.model(frame, verbose=False)[0]
    
                label = result.names[result.probs.top1]
                confidence = float(result.probs.top1conf)
    
                now = time.time()
    
                            
                if confidence > CONFIDENCE_THRESHOLD and label != "nothing":
                    if now - self.last_process_time > 2:  # debounce 2 seconds
                        self.last_process_time = now
                        print(f"Detected: {label}")
                        self.ars.process_trash(label)
    
                self.ars.process_trash(label)
    
                self.busy = False
                self.counter = 0
            except Exception as e:
                print("AI LOOP ERROR:", e)
                time.sleep(0.5)