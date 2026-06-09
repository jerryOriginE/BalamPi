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

    def set_angle(self, angle):
        self.servo1.angle = angle

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

CALIBRATE_ARM_ANGLE = 90
CALIBRATE_PIVOT_ANGLE = 0

POSITIONS = {
    "back_right": (100, 90),
    "front_left": (80, 0),
    "back_left": (100, 90),
    "front_right": (80, 90)
}

class Controller:
    def __init__(self, arm_servo1, arm_servo2, pivot_servo):
        self.arm = ArmController(arm_servo1, arm_servo2)
        self.pivot = PivotController(pivot_servo)

    def dettach_servos(self):
        sleep(0.5)
        self.arm.dettach()
        self.pivot.dettach()

    def calibrate(self):
        print("Calibrating servos to start position...")
        self.arm.set_angle(CALIBRATE_ARM_ANGLE)
        self.pivot.set_angle(CALIBRATE_PIVOT_ANGLE)
    
        self.dettach_servos()

    def move_to(self, position):
        self.calibrate()

        print(f"Moving to {position}...")
        self.pivot.set_angle(POSITIONS[position][1])
        sleep(1)
        self.arm.set_angle(POSITIONS[position][0])

        self.dettach_servos()

def main():
    controller = Controller(18, 19, 20)
    controller.calibrate()
    sleep(2)

    controller.move_to("back_right")

if __name__ == "__main__":    main()