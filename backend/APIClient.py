# backend/APIClient.py
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def verify_user(self, qr_data):
        response = requests.post(
            f"{self.base_url}/auth/verify-user",
            json=qr_data,
            timeout=5
        )
        print(f"API Response: {response.status_code}, {response.text}")
        return response.json()

    def award_points(self, user_id, waste_type):
        response = requests.post(
            f"{self.base_url}/auth/award-points",
            json={
                "userId": user_id, 
                "wasteType": waste_type
                },
            timeout=5
        )

        print(f"API Response: {response.status_code}, {response.text}")
        return response.json()

    def end_session(self, user_id):
        response = requests.post(
            f"{self.base_url}/auth/end-session",
            json={
                "userId": user_id
            },
            timeout=5
        )

        print(f"API Response: {response.status_code}, {response.text}")
        return response.json()