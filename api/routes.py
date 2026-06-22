from hardware.lcd import lcd
from flask import request, jsonify
import requests
from config import BACKEND_URL
from hardware.QRScanner import QRScanner

def setup_routes(app, ai, session):

    scanner = QRScanner()

    @app.get("/")
    def home():
        return {"message": "ARS Online"}

    @app.route('/button')
    def button():
        print("Button Pressed")

        qr_data = scanner.scan()

        if qr_data is None:
            return {"status": "no_qr"}
        
        print(f"QR Data: {qr_data}")

        try:
            response = requests.post(
                BACKEND_URL + "/auth/verify-user",
                json=qr_data,
                timeout=5
            )

            result = response.json()
            print(f"Verification Result: {result}")
            lcd("Verification Result: " + str(result))

        except Exception as e:
            print(f"Error verifying user: {e}")
            lcd("Verification Failed")
            return {"status": "error"}
        
        if result.get("valid"):
            user = result["user"]

            print(f"User {user['name']} verified successfully")
            lcd(f"Welcome {user['name']}")

            session.start(user)
            ai.start()

            return {"status": "started", "user": user}

        lcd("Access Denied")
        return jsonify({"status": "denied"}), 401