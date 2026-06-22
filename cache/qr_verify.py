import requests
import subprocess

response = requests.post(
    "http://localhost:5000/auth/verify-user",
    json=payload
)

data = response.json()

if data.get("valid"):

    subprocess.Popen([
        "/home/gerardo/BalamPi/.venv/bin/python",
        "/home/gerardo/BalamPi/waste_camera.py"
    ])

    print("Verification successful")
else:
    print("Verification failed")