# ars/ARS.py
from controllers.RecycleController import ARS as HardwareARS

class ARS:
    def __init__(self, lcd):
        self.controller = HardwareARS(lcd=lcd)

    def calibrate(self):
        self.controller.calibrate_system()

    def process(self, trash_type):
        self.controller.process_trash(trash_type)

    def map_type(self, trash_type, position):
        self.controller.change_trash_data(trash_type, position)