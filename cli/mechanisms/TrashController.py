# lets turn this into a full single class controller
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




#
POSITONS = {}
with open('settings/TrashPositions.txt') as f:
    for line in f:
        key, value = line.strip().split('=')
        POSITONS[key] = int(value)
    #print(f"Extracted positions: {POSITONS}")

class TrashController:
    def __init__(self, arm_servo1, arm_servo2, pivot_servo, debug=False):
        self.debug = debug

        if self.debug:
            print("Debug mode: servos will not be moved.")
            return
        
        print(f"Initializing TrashController with arm servos on GPIO {arm_servo1} and {arm_servo2}, pivot servo on GPIO {pivot_servo}")
        self.arm = ArmController(arm_servo1, arm_servo2)
        self.pivot = PivotController(pivot_servo)

    def calibrate(self):
        print("Calibrating servos to start position...")
        if self.debug:
            print("Debug mode: skipping actual servo movement.")
            return
        self.arm.set_angle(90)
        self.pivot.set_angle(50)

    def move_back_right(self):
        print("Moving to back right...")
        if self.debug:
            print("Debug mode: skipping actual servo movement.")
            return
        self.arm.set_angle(POSITONS['arm_pos'])
        self.pivot.set_angle(POSITONS['pivot_pos'])

    def move_front_left(self):
        print("Moving to front left...")
        if self.debug:
            print("Debug mode: skipping actual servo movement.")
            return
        self.arm.set_angle(POSITONS['arm_rev_pos'])
        self.pivot.set_angle(POSITONS['pivot_pos'])

    def move_back_left(self):
        print("Moving to back left...")
        if self.debug:
            print("Debug mode: skipping actual servo movement.")
            return
        self.arm.set_angle(POSITONS['arm_pos'])
        self.pivot.set_angle(POSITONS['pivot_rev_pos'])

    def move_front_right(self):
        print("Moving to front right...")
        if self.debug:
            print("Debug mode: skipping actual servo movement.")
            return
        self.arm.set_angle(POSITONS['arm_rev_pos'])
        self.pivot.set_angle(POSITONS['pivot_rev_pos'])
