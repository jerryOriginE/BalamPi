# app.py

from flask import Flask
from controllers.RecycleController import ARS, Position
from WasteAI import WasteAI

app = Flask(__name__)

# Create once
ARS_system = ARS()
ARS_system.change_trash_data("plastic", Position.BACK_RIGHT)
ARS_system.change_trash_data("trash", Position.FRONT_LEFT)
ARS_system.change_trash_data("cardboard", Position.BACK_LEFT)
ARS_system.change_trash_data("metal", Position.FRONT_RIGHT)

# Create once
waste_ai = WasteAI(ARS_system)

@app.route("/start-session", methods=["POST"])
def start_session():
    waste_ai.start()
    return {"message": "Session started"}

@app.route("/stop-session", methods=["POST"])
def stop_session():
    waste_ai.stop()
    return {"message": "Session stopped"}

if __name__ == "__main__":
    waste_ai.run_background()
    app.run(host="0.0.0.0", port=6000)


