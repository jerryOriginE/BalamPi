from gpiozero import AngularServo
from time import sleep

class Servo:
    def __init__(self, pin, min_angle=-180, max_angle=180, min_pulse_width=0.0009, max_pulse_width=0.0021):
        self.servo = AngularServo(
            pin,
            initial_angle=0,
            min_angle=min_angle,
            max_angle=max_angle,
            min_pulse_width=0.000,
            max_pulse_width=0.0026
        )

    def set_angle(self, angle):
        self.servo.angle = angle

# so we got a issue each door hanlde has two servos, one is opposite to the other bc the door moves with two hinges each hinge is attached to the servo so for one to open one servo need st ortate for say 45 deggres and the other needs to rotate 45 in the opposite direction
# so whats the best way to achieved this

## what i am planning is that set all servos two 0 with code and whateve rposition is that hpyiscal attach the hinge there when it should be closed


OPEN_ANGLE = 180 # -180
CLOSE_ANGLE = 0

class Door():
    def __init__(self, servo1, servo2, inverted=False):
        self.servo1 = Servo(servo1)
        self.servo2 = Servo(servo2)
        self.inverted = inverted

    def detach(self):
        sleep(0.5)
        self.servo1.detach()
        self.servo2.detach()

    def calibrate(self):
        self.servo1.set_angle(CLOSE_ANGLE)
        self.servo2.set_angle(CLOSE_ANGLE)

    def open(self):
        if not self.inverted:
            self.servo1.set_angle(OPEN_ANGLE)
            self.servo2.set_angle(-OPEN_ANGLE)
        else:
            self.servo1.set_angle(-OPEN_ANGLE)
            self.servo2.set_angle(OPEN_ANGLE)

        #self.detach()

    def close(self):
        self.servo1.set_angle(CLOSE_ANGLE)
        self.servo2.set_angle(CLOSE_ANGLE)

        #self.detach()

class DoorController():
    def __init__(self, servo1, servo2, servo3, servo4, door1_inverted, door2_inverted):
        print("Initializing DoorController with servos:", servo1, servo2, servo3, servo4)
        self.door1 = Door(servo1, servo2, door1_inverted)
        self.door2 = Door(servo3, servo4, door2_inverted)

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
