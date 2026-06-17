from controllers.TrashController import Controller
from time import sleep

def main():
    controller = Controller(27, 22)
    controller.calibrate()

if __name__ == "__main__":    main()