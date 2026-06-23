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
        sleep(0.5)  # wait for servo to reach the desired angle
        self.servo.detach()  # detach the servo to prevent jittering after movement

    def dettach(self):
        self.servo.detach()

class ArmController:
    def __init__(self, servo1):
        self.servo1 = Servo(servo1)

    def set_angle(self, angle):
        self.servo1.set_angle(angle)


class PivotController:
    def __init__(self, servo):
        self.servo = Servo(servo)

    def set_angle(self, angle):
        self.servo.set_angle(angle)

CALIBRATE_ARM_ANGLE = 0
CALIBRATE_PIVOT_ANGLE = 0.5

POSITIONS = {
    "back_right": (0.5, 0),
    "front_left": (-0.5, 0),
    "back_left": (0.5, -1),
    "front_right": (-0.5, -1)
}

class Controller:
    def __init__(self, arm_servo1, pivot_servo):
        self.arm = ArmController(arm_servo1)
        self.pivot = PivotController(pivot_servo)

    def calibrate(self):
        print("\nCalibrating servos to start position...")
        self.arm.set_angle(CALIBRATE_ARM_ANGLE)
        self.pivot.set_angle(CALIBRATE_PIVOT_ANGLE)

    def move_to(self, position):
        self.calibrate()

        print(f"Moving to {position}...")
        self.pivot.set_angle(POSITIONS[position][1])
        #sleep(0.5)
        self.arm.set_angle(POSITIONS[position][0])
        sleep(1)
        self.calibrate()
        sleep(0.5)
