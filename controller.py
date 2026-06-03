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


arm_pos=45
pivot_pos=0
arm_rev_pos=100
pivot_rev_pos=160

class Controller:
    def __init__(self, arm_servo1, arm_servo2, pivot_servo):
        self.arm = ArmController(arm_servo1, arm_servo2)
        self.pivot = PivotController(pivot_servo)

    def calibrate(self):
        print("Calibrating servos to start position...")
        self.arm.set_angle(90)
        self.pivot.set_angle(50)

    def move_back_right(self):
        print("Moving to back right...")
        self.arm.set_angle(arm_pos)
        self.pivot.set_angle(pivot_pos)

    def move_front_left(self):
        print("Moving to front left...")
        self.arm.set_angle(arm_rev_pos)
        self.pivot.set_angle(pivot_pos)

    def move_back_left(self):
        print("Moving to back left...")
        self.arm.set_angle(arm_pos)
        self.pivot.set_angle(pivot_rev_pos)

    def move_front_right(self):
        print("Moving to front right...")
        self.arm.set_angle(arm_rev_pos)
        self.pivot.set_angle(pivot_rev_pos)

def main():
    controller = Controller(18, 19, 20)
    controller.calibrate()
    sleep(2)

    while True:
        controller.move_back_right()
        sleep(1)
        controller.move_front_left()
        sleep(1)
        controller.move_back_left()
        sleep(1)
        controller.move_front_right()
        sleep(1)
        controller.calibrate()
        sleep(1)

if __name__ == "__main__":    main()