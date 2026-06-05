from registry import register
from time import sleep
import sys
import os

def general_info():
    print("This command allows you to move a servo to a specific angle.")
    print("Usage: move_servo <gpio_pin> <angle> [--dry-run]")
    print("Example: move_servo 17 90 --dry-run")


@register('move_servo')
def move_servo(args):
    if not args or len(args) < 2:
        general_info()
        return

    dry_run = False
    if '--dry-run' in args:
        dry_run = True
        args = [a for a in args if a != '--dry-run']

    pin_arg = args[0]
    angle_arg = args[1]

    try:
        pin = int(pin_arg)
    except ValueError:
        print(f"Invalid GPIO pin: {pin_arg}")
        return

    try:
        angle = int(angle_arg)
    except ValueError:
        print(f"Invalid angle: {angle_arg}")
        return

    # clamp angle
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180

    print(f"Moving servo {pin} to position: {angle} (dry_run={dry_run})")

    if dry_run:
        print("Dry-run: skipping hardware interaction")
        return

    try:
        from gpiozero import AngularServo
    except Exception as e:
        print(f"gpiozero not available or failed to import: {e}")
        return

    try:
        servo = AngularServo(
            pin,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025,
        )
        servo.angle = angle
        sleep(1)
        # detach if available
        if hasattr(servo, 'detach'):
            try:
                servo.detach()
            except Exception:
                pass
        sleep(0.1)
        # close the device
        if hasattr(servo, 'close'):
            try:
                servo.close()
            except Exception:
                pass
    except Exception as e:
        print(f"Failed to move servo: {e}")