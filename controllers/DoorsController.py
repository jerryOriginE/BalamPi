from gpiozero import Servo
from time import sleep

class DoorServo():
    def __init__(self, pin, min_pulse_width=0.0005, max_pulse_width=0.0025, inverted=False):
        self.pin = pin
        self.min_pulse_width = min_pulse_width
        self.max_pulse_width = max_pulse_width
        self.inverted = inverted

        self.servo = Servo(
            self.pin,
            min_angle=-180,
            max_angle=180,
            min_pulse_width=self.min_pulse_width,
            max_pulse_width=self.max_pulse_width
        )
        print(f"Initialized servo on pin {self.pin} with pulse widths {self.min_pulse_width} to {self.max_pulse_width}")

    def set_angle(self, angle):
        if angle < -1 or angle > 1:
            raise ValueError("Angle must be between -1 and 1")
        
        if self.inverted:
            angle = -angle
        
        self.servo.value = angle

    def detach(self):
        self.servo.detach()

CLOSE_ANGLE = -1
OPEN_ANGLE = 0

class Door():
    def __init__(self, servo1, servo2, inverted=False):
        self.servo1 = DoorServo(servo1, inverted=False)
        self.servo2 = DoorServo(servo2, inverted=True)
        self.inverted = inverted

    def stop_servos(self):
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

        sleep(1)
        self.stop_servos()

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
