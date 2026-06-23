from controllers.RecycleController import ARS, Position
from ai.WasteAI import WasteAI
from auth.SessionManager import SessionManager
from api.server import create_server
from hardware.lcd import lcd
from config import SERVER_PORT
import time


lcd("Booting... - ARS-os.v1.4.2")

ars = ARS()

ars.change_trash_data("plastic", Position.BACK_RIGHT)
ars.change_trash_data("trash", Position.FRONT_LEFT)
ars.change_trash_data("cardboard", Position.BACK_LEFT)
ars.change_trash_data("metal", Position.FRONT_RIGHT)

ars.calibrate_system()

session = SessionManager()


ai = WasteAI(ars, session)

app = create_server(ai, session)

ai.run_background()


time.sleep(1)
lcd("System Ready")


app.run(host="0.0.0.0", port=SERVER_PORT)