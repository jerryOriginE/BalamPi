from gpiozero import AngularServo
from time import sleep

servo = AngularServo(
    18,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

servo2 = AngularServo(
    19,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

sleep(1)

servo.angle = 0
servo2.angle = 0

sleep(1)

servo.detach()
servo2.detach()

servo.angle = 90
servo2.angle = 180

sleep(1)