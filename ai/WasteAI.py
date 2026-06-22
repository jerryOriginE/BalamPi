from ultralytics import YOLO
import cv2
import time
import threading
from config import AI_MODEL, CAMERA_INDEX, AI_TIMEOUT, CONFIDENCE_THRESHOLD

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

    def start(self):
        if self.active:
            return
        
        print("AI  Started")
        self.active = True
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

    def stop(self):
        print("AI Stopped")
        self.active = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def run_background(self):
        thread = threading.Thread(
            target=self.loop,
            daemon=True
        )

        thread.start()

    def loop(self):
        while True:
            if not self.active:
                time.sleep(0.1)
                continue

            ret, frame = self.cap.read()
            if not ret:
                continue

            result = self.model(frame, verbose=False)[0]

            label = result.names[result.probs.top1]
            confidence = float(result.probs.top1conf)

            if confidence < CONFIDENCE_THRESHOLD or label == "nothing":
                continue
        
            if self.busy:
                continue

            if label == self.last_lalbel:
                self.counter += 1
            else:
                self.last_lalbel = label
                self.counter = 0

            if self.counter >= 10:
                self.busy = True
                print(f"Detected: {label} with confidence {confidence:.2f}")

            self.ars.process_trash(label)

            self.busy = False
            self.counter = 0