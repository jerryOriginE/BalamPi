from registry import register
from gpiozero import AngularServo
from time import sleep

def general_info():
    print("This command allows you to move a servo to a specific angle.")
    print("Usage: move_servo <gpio_pin> <angle>")
    print("Example: move_servo 17 90")

@register('move_servo')
def move_servo(args):
    if not args or len(args) < 2:
        general_info()
        return
    
    print(f"Moving servo {args[0]} to position: {args[1]}")

    servo_gpio = args[0]

    servo = AngularServo(
            servo_gpio,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )
    angle = int(args[1])
    servo.angle = angle
    sleep(1)
    servo.detach()

    sleep(0.1)

    # delete it once finished
    servo.close()