# lets turn this into a full single class controller
from gpiozero import AngularServo
from time import sleep

class Servo:
    def __init__(self, pin, min_pulse_width=0.0005, max_pulse_width=0.0025):
        self.servo = AngularServo(
            pin,
            min_pulse_width=min_pulse_width,
            max_pulse_width=max_pulse_width
        )

    def set_angle(self, angle):
        print(f"Setting servo angle to {angle}")
        self.servo.value = angle

    def dettach(self):
        self.servo.detach()


servo1 = Servo(27)

servo1.set_angle(0)

print("Testing servo movement...")

sleep(2)
servo1.set_angle(0.5)
sleep(2)
servo1.set_angle(-0.5)
sleep(3)