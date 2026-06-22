from flask import Flash
import subprocess

app = Flask(__name__)

# stuff
VENV_PYTHON = "/home/gerardo/BalamPi/.venv/bin/python"
SCRIPT_PATH = "/home/gerardo/BalamPi/waste_camera.py"

def waste_camera_running():
    result = subprocess.run(
        ["pgrep", "-f", "waste_camera.py"],
        capture_output=True,
        text=True
    )

    return result.returncode == 0

@app.route('/button', methods=['POST'])
def button():
    print("ESP32 button pressed!")

    # do stuff
    if waste_camera_running():
        print("waste_camera.py is already running.")
        return "Already running"
    
    print("Starting waste_camera.py...")

    subprocess.Popen([
        VENV_PYTHON,
        "/home/gerardo/BalamPi/qr_verify.py"
    ])

    return "Verification Started"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)