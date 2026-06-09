from gpiozero import AngularServo
from time import sleep

# custom controller using two servos for an arm, both should work as one but one is opposite of the other, so one should be 180 - the angle of the other
class ArmController:
    def __init__(self, servo1, servo2):
        self.servo1 = AngularServo(
            servo1,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )
        self.servo2 = AngularServo(
            servo2,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )

    def set_angle(self, angle):
        self.servo1.angle = angle
        self.servo2.angle = 180 - angle

class PivotController:
    def __init__(self, servo):
        self.servo = AngularServo(
            servo,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0009,
            max_pulse_width=0.0021
        )

    def set_angle(self, angle):
        self.servo.angle = angle

arm = ArmController(18, 19)
pivot = PivotController(20)

# go to start position
arm.set_angle(140)
pivot.set_angle(0)

sleep(5)

while True:
    for angle in range(0, 181, 10):
        print(f"Setting angle to {angle}")
        arm.set_angle(angle)
        pivot.set_angle(angle)
        sleep(0.5)
    sleep(1.5)