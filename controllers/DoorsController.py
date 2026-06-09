from gpiozero import AngularServo
from time import sleep

class Servo:
    def __init__(self, pin, min_angle=0, max_angle=180, min_pulse_width=0.0009, max_pulse_width=0.0021):
        self.servo = AngularServo(
            pin,
            min_angle=min_angle,
            max_angle=max_angle,
            min_pulse_width=min_pulse_width,
            max_pulse_width=max_pulse_width
        )

    def set_angle(self, angle):
        self.servo.angle = angle
        sleep(0.5)
        #self.dettach()

    def dettach(self):
        self.servo.detach()

# so we got a issue each door hanlde has two servos, one is opposite to the other bc the door moves with two hinges each hinge is attached to the servo so for one to open one servo need st ortate for say 45 deggres and the other needs to rotate 45 in the opposite direction
# so whats the best way to achieved this

## what i am planning is that set all servos two 0 with code and whateve rposition is that hpyiscal attach the hinge there when it should be closed


OPEN_ANGLE = 90
CLOSE_ANGLE = 0

class Door():
    def __init__(self, servo1, servo2):
        self.servo1 = Servo(servo1)
        self.servo2 = Servo(servo2)

    def calibrate(self):
        self.servo1.set_angle(0)
        self.servo2.set_angle(0)

    def open(self):
        self.servo1.set_angle(OPEN_ANGLE)
        self.servo2.set_angle(180 - OPEN_ANGLE)

    def close(self):
        self.servo1.set_angle(CLOSE_ANGLE)
        self.servo2.set_angle(180 - CLOSE_ANGLE)

class DoorController():
    def __init__(self, servo1, servo2, servo3, servo4):
        print("Initializing DoorController with servos:", servo1, servo2, servo3, servo4)
        self.door1 = Door(servo1, servo2)
        #self.door2 = Door(servo3, servo4)

    def calibrate(self):
        print("Calibrating doors...")
        self.door1.calibrate()
        #self.door2.calibrate()


    def open_doors(self):
        print("Opening doors...")
        self.door1.open()
        #self.door2.open()

    def close_doors(self):
        print("Closing doors...")
        self.door1.close()
        #self.door2.close()
