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

# so the key concept behind this is that the arm and pivot work in sync to achieve 4 differnet ouputs, its a plate that rotaes and moves up and down whenver it moves it should drop the items in one of four sides
# so we need to amek some sort of inverse kimeatics to figure out the angles for the arm and pivot to achieve the desired output
# for example if we want to drop the item in the front right corner we need to move the pivot 45 deegres and the in one side which coudl be up or down

# but first we need to make some sort of calibration of teh servos

# go to start position
def calibrate_servos():
    print("Calibrating servos to start position...")
    arm.set_angle(90)
    pivot.set_angle(50)

calibrate_servos()
sleep(2)

arm_pos=45
pivot_pos=0
arm_rev_pos=100
pivot_rev_pos=160

def move_back_right():
    print("Moving to back right...")
    arm.set_angle(arm_pos)
    pivot.set_angle(pivot_pos)

#due to teh way the system is the pivot can be the same and we juts invert the arm angles to achieve the opposite side
def move_front_left():
    print("Moving to front left...")
    arm.set_angle(arm_rev_pos)
    pivot.set_angle(pivot_pos)

def move_back_left():
    print("Moving to back left...")
    arm.set_angle(arm_pos)
    pivot.set_angle(pivot_rev_pos)

def move_front_right():
    print("Moving to front right...")
    arm.set_angle(arm_rev_pos)
    pivot.set_angle(pivot_rev_pos)

move_back_right()
sleep(2)
move_front_left()
sleep(2)
move_back_left()
sleep(2)
move_front_right()

print("Done with movements, resetting to start position...")
sleep(2)

calibrate_servos()
sleep(1)
