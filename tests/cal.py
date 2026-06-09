from TrashController import Controller
from time import sleep

def main():
    controller = Controller(16, 26)
    controller.calibrate()

if __name__ == "__main__":    main()