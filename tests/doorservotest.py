from gpiozero import AngularServo
from time import sleep

class Servo:
    def __init__(self, pin, min_angle=-180, max_angle=180, min_pulse_width=0.0009, max_pulse_width=0.0021):
        self.servo = AngularServo(
            pin,
            initial_angle=0,
            min_angle=min_angle,
            max_angle=max_angle,
            min_pulse_width=0.0004,
            max_pulse_width=0.0026
        )

    def set_angle(self, angle):
        self.servo.angle = angle
        
        
servo = Servo(16)

servo.set_angle(-180)
sleep(3)

servo.set_angle(0)
sleep(3)

servo.set_angle(180)
sleep(3)