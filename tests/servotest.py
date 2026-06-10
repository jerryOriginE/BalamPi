from gpiozero import AngularServo
from time import sleep

servo = AngularServo(
    16,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

while True:
    servo.angle = 0
    sleep(1)
    servo.angle = 90
    sleep(1)
    servo.angle = 180
    sleep(1)