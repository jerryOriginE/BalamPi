from controllers.DoorsController import DoorController
from time import sleep

import sys

# to faciliate tesing lets do so depenidng on the arguments of the python testdoors.py different things thappend
# testonce
# testloop
# calibrate

if len(sys.argv) < 2:
    print("Usage: python testdoors.py [testonce|testloop|calibrate]")
    sys.exit(1)

controller = DoorController(26, 16, 5, 6, False, False)
    
#controller.calibrate()
sleep(1)

if sys.argv[1] == "testonce":
    controller.open_doors()
    sleep(1)
    controller.close_doors()
    sleep(2)

elif sys.argv[1] == "testloop":
    for _ in range(5):
        controller.open_doors()
        sleep(1)
        controller.close_doors()
        sleep(1)

elif sys.argv[1] == "calibrate":
    controller.calibrate()
    sleep(1)

elif sys.argv[1] == "testdoors":
    controller.test_doors()
    sleep(1)