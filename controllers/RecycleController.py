from controllers.TrashController import Controller
from controllers.DoorsController import DoorController
from time import sleep
from enum import Enum
import requests


class Status(Enum):
    IDLE = 'idle'
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class Position(Enum):
    BACK_LEFT = 'back_left'
    BACK_RIGHT = 'back_right'
    FRONT_LEFT = 'front_left'
    FRONT_RIGHT = 'front_right'

# here wer acess a unique string to a Postion enum this can be changed with a def later
TRASH_DATA = {
    "Plastic": Position.BACK_RIGHT,
    "Tetrabrik": Position.FRONT_LEFT,
    "Paper/Cardbord": Position.BACK_LEFT,
    "Metal": Position.FRONT_RIGHT
}

# so the key idea behind te controller is multiple components working in sync, the RecycleCOntroller would receive something like recycle_controller.process_trash('TRASH_NAME')
# the controllwer will receive this it wil decide in which position to deposite and the na sequence of events happends
# the doors .open() the the trash_controllers move.to(position) and the doors close() after this the systems can be trigged agian but durin the whole proces the different Status enums will change letting know the user the current state so it cant get overrun
# the controller will also have a calibrate() function that will calibrate all the components to their start position, this can be called at the start of the program or after a certain number of cycles to ensure everything is in the right position

class RecycleController:
    def __init__(self):
        self.trash_controller = Controller(27, 22)
        self.doors_controller = DoorController(26, 16, 5, 6, False, False)
        self.status = Status.IDLE
        self.trash_data = TRASH_DATA

    def change_trash_data(self, trash_type, position):
        # check if the format is correct as a string and position enum
        if not isinstance(trash_type, str) or not isinstance(position, Position):
            print("Invalid input format. Trash type should be a string and position should be a Position enum.")
            return
        
        self.trash_data[trash_type] = position
        print(f"Updated trash data: {trash_type} -> {position.value}")

    def calibrate(self):
        self.trash_controller.calibrate()
        self.doors_controller.close_doors()
        sleep(1)

    def process_trash(self, trash_type):
        if self.status != Status.IDLE:
            print("System is busy processing another trash, please wait...")
            return

        self.status = Status.PENDING
        print(f"Processing {trash_type}...")

        position = self.trash_data.get(trash_type)
        if not position:
            print(f"Unknown trash type: {trash_type}")
            self.status = Status.IDLE
            return
        self.status = Status.IN_PROGRESS
        
        print(f"Current status: {self.status.name}, Processing: {trash_type}, Next position: {position.value}, Next action: Open doors")
        #lcd(f"Processing {trash_type}...")  # update LCD with current processing status

        self.trash_controller.calibrate()  # ensure trash controller is in start position before moving

        sleep(1)  # wait for calibration to complete
        self.doors_controller.open_doors()

        print(f"Current status: {self.status.name}, Processing: {trash_type}, Next position: {position.value}, Next action: Move trash to position")
        #lcd(f"Status: {self.status.name}")
        sleep(1)  # wait for doors to open

        self.trash_controller.move_to(position.value)

        print(f"Current status: {self.status.name}, Processing: {trash_type}, Next position: {position.value}, Next action: Close doors")
        #lcd(f"Status: {self.status.name}")
        sleep(1)  # wait for trash to be moved

        self.doors_controller.close_doors()

        print(f"Current status: {self.status.name}, Processing: {trash_type}, Next position: {position.value}, Next action: Wait for doors to close")
        #lcd(f"Status: {self.status.name}")
        sleep(1)  # wait for doors to close

        self.status = Status.COMPLETED
        print(f"Finished processing {trash_type}. Current status: {self.status.name}")
        #lcd(f"Status: {self.status.name}")

        print("System is now idle and ready for next trash.")
        #lcd(f"Status: {self.status.name}")
        self.status = Status.IDLE

class ARS():
    def __init__(self):
        self.recycle_controller = RecycleController()

    def calibrate_system(self):
        self.recycle_controller.calibrate()

    def process_trash(self, trash_type):
        self.recycle_controller.process_trash(trash_type)

    def change_trash_data(self, trash_type, position):
        self.recycle_controller.change_trash_data(trash_type, position)

'''
def main():
    recycle_controller = RecycleController()
    recycle_controller.calibrate()

    print("Calibrating please wait...")
    sleep(3)

    # test
    recycle_controller.process_trash('paper')
'''

#if __name__ == "__main__":    main()


