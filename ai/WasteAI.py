from ultralytics import YOLO
import cv2
import time
import threading
import numpy as np
from config import AI_MODEL, AI_CAMERA_PATH, CONFIDENCE_THRESHOLD

class WasteAI:
    def __init__(self, ars, session):
        self.ars = ars
        self.session = session

        self.model = YOLO(AI_MODEL)

        self.active = False
        self.cap = None

        self.lock = threading.Lock()
        self.last_process_time = 0

        self.current_label = "waiting..."
        self.current_conf = 0.0

        self.show_processing_screen = False
        self.processing_label = None

    # ---------------- START / STOP ----------------

    def start(self):
        with self.lock:
            if self.active:
                return

            self.active = True

            if self.cap:
                self.cap.release()

            self.cap = cv2.VideoCapture(0)
            time.sleep(0.5)

            print("AI Started")

    def stop(self):
        with self.lock:
            self.active = False

        if self.cap:
            self.cap.release()
            self.cap = None

        cv2.destroyAllWindows()
        print("AI Stopped")

    # ---------------- BACKGROUND ----------------

    def run_background(self):
        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()

    # ---------------- UI SCREEN ----------------

    def show_processing(self, label):
        screen = np.zeros((720, 1280, 3), dtype=np.uint8)

        cv2.putText(screen,
                    "PROCESSING ITEM",
                    (250, 250),
                    cv2.FONT_HERSHEY_DUPLEX,
                    2,
                    (0, 255, 255),
                    3)

        cv2.putText(screen,
                    label.upper(),
                    (350, 400),
                    cv2.FONT_HERSHEY_DUPLEX,
                    3,
                    (0, 255, 0),
                    5)

        cv2.imshow("ARS Status", screen)
        cv2.waitKey(1)

    # ---------------- MAIN LOOP ----------------

    def loop(self):
        while True:
            try:
                if not self.active:
                    time.sleep(0.1)
                    continue

                ret, frame = self.cap.read()
                if not ret or frame is None:
                    continue

                # ---------------- MODEL ----------------
                result = self.model(frame, verbose=False)[0]

                if result.probs is None:
                    continue

                class_id = result.probs.top1
                confidence = float(result.probs.top1conf)
                label = result.names[class_id]

                self.current_label = label
                self.current_conf = confidence

                # ---------------- DISPLAY FEED ----------------
                text = f"{label}: {confidence*100:.1f}%"

                cv2.putText(frame,
                            text,
                            (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2)

                cv2.putText(frame,
                            "©BALAM - ARS 2026",
                            (20, frame.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 255),
                            1)

                cv2.imshow("Waste AI Feed", frame)
                cv2.waitKey(1)

                # ---------------- DECISION ----------------
                now = time.time()

                if confidence > CONFIDENCE_THRESHOLD and label != "nothing":
                    if now - self.last_process_time > 2:

                        self.last_process_time = now

                        print(f"Detected: {label}")

                        # show processing screen
                        self.show_processing(label)

                        # send to robot
                        self.ars.process_trash(label)

                        time.sleep(1)

                        cv2.destroyWindow("ARS Status")

                time.sleep(0.01)

            except Exception as e:
                print("AI LOOP ERROR:", e)
                time.sleep(0.5)