from DoorsController import DoorController
from time import sleep

def main():
    controller = DoorController(16, 26, 20, 21)

    controller.calibrate()
    #
    #sleep(1)
    controller.open_doors()

    sleep(1)

    #controller.close_doors()

if __name__ == "__main__":    main()