from controllers.TrashController import Controller
from time import sleep

import sys

# to faciliate tesing lets do so depenidng on the arguments of the python testdoors.py different things thappend
# testonce
# testloop
# calibrate

if len(sys.argv) < 2:
    print("Usage: python testsys.py [back_right|front_left|back_left|front_right|testloop|calibrate]")
    sys.exit(1)

controller = Controller(27, 22)

sleep(1)

if sys.argv[1] == "back_right":
    controller.move_to("back_right")

elif sys.argv[1] == "front_left":
    controller.move_to("front_left")

elif sys.argv[1] == "back_left":
    controller.move_to("back_left")

elif sys.argv[1] == "front_right":
    controller.move_to("front_right")

elif sys.argv[1] == "testloop":
    controller.move_to("back_right")
    controller.move_to("front_left")
    controller.move_to("back_left")
    controller.move_to("front_right")

elif sys.argv[1] == "calibrate":
    controller.calibrate()
    sleep(1)
