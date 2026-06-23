from controllers.TrashController import Controller
from time import sleep

def main():
    controller = Controller(27, 22)

    controller.calibrate()
    sleep(3)
    controller.move_to("back_right")
    controller.move_to("front_left")
    controller.move_to("back_left")
    controller.move_to("front_right")

if __name__ == "__main__":    main()
