# core/SystemController.py
import threading
import time

from core.StateMachine import State

class SystemController:
    def __init__(
            self,
            esp32,
            lcd,
            auth,
            api,
            session,
            ai,
            processor
    ):
        self.esp32 = esp32
        self.lcd = lcd
        self.auth = auth
        self.api = api
        self.session = session
        self.ai = ai
        self.processor = processor

        self.state = State.IDLE

    def start(self):
        self.esp32.on_button(
            self.handle_button
        )

        self.esp32.start()

        threading.Thread(
            target=self.ai_loop,
            daemon=True
        ).start()

        
        threading.Thread(
            target=self.session_loop,
            daemon=True
        ).start()

        self.lcd.show("System Ready")

    def handle_button(self):

        if self.state != State.IDLE:
            return

        self.state = State.WAITING_QR

        self.lcd.show("Scan QR")

        user = self.auth.authenticate()

        if not user:

            self.state = State.IDLE

            self.lcd.show(
                "Authentication Failed"
            )

            return

        self.session.start(user)

        self.state = State.ACTIVE

        self.lcd.show(
            f"Welcome {user['username']}"
        )

    def ai_loop(self):
        print("AI thread started")

        while True:
            if self.state != State.ACTIVE:
                time.sleep(0.2)
                continue

            print("ACTIVE")

            label = self.ai.detect()

            print("Detected:", label)

            if label:
                print("Processing:", label)
                self.processor.process(label)

    def session_loop(self):
        while True:
            if (
                self.session.active and
                self.session.expired()
            ):
                self.api.end_session(self.session.user["id"])
                self.session.stop()
                self.state = State.IDLE
                self.lcd.show("Session Ended")

            time.sleep(1)