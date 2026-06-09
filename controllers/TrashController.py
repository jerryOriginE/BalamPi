# lets turn this into a full single class controller
from gpiozero import AngularServo
from time import sleep

class Servo:
    def __init__(self, pin, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025):
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
        self.dettach()

    def dettach(self):
        self.servo.detach()

# custom controller using two servos for an arm, both should work as one but one is opposite of the other, so one should be 180 - the angle of the other
class ArmController:
    def __init__(self, servo1):
        self.servo1 = Servo(servo1)

    def set_angle(self, angle):
        self.servo1.set_angle(angle)


class PivotController:
    def __init__(self, servo):
        self.servo = Servo(
            servo,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0009,
            max_pulse_width=0.0021
        )

    def set_angle(self, angle):
        self.servo.set_angle(angle)

ARM_OFFSET = 19

CALIBRATE_ARM_ANGLE = 90
CALIBRATE_PIVOT_ANGLE = 0

POSITIONS = {
    "back_right": (130, 45),
    "front_left": (30, 45),
    "back_left": (130, 180),
    "front_right": (30, 180)
}

class Controller:
    def __init__(self, arm_servo1, pivot_servo):
        self.arm = ArmController(arm_servo1)
        self.pivot = PivotController(pivot_servo)

    def calibrate(self):
        print("\nCalibrating servos to start position...")
        self.arm.set_angle(CALIBRATE_ARM_ANGLE + ARM_OFFSET)
        self.pivot.set_angle(CALIBRATE_PIVOT_ANGLE)

    def move_to(self, position):
        self.calibrate()

        print(f"Moving to {position}...")
        self.pivot.set_angle(POSITIONS[position][1])
        #sleep(0.5)
        self.arm.set_angle(POSITIONS[position][0] + ARM_OFFSET)
        sleep(1)
        self.calibrate()
        sleep(0.5)
