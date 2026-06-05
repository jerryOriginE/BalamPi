# lets turn this into a full single class controller
from gpiozero import AngularServo
from time import sleep
from time import sleep
import os


# custom controller using two servos for an arm
class ArmController:
    def __init__(self, servo_pin1, servo_pin2, debug=False):
        self.debug = debug
        self.servo1 = None
        self.servo2 = None
        if self.debug:
            return

        try:
            from gpiozero import AngularServo
        except Exception as e:
            raise ImportError(f"gpiozero AngularServo not available: {e}")

        self.servo1 = AngularServo(
            servo_pin1,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025,
        )
        self.servo2 = AngularServo(
            servo_pin2,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025,
        )

    def set_angle(self, angle):
        if self.debug:
            print(f"[debug] ArmController.set_angle({angle})")
            return
        if self.servo1:
            self.servo1.angle = angle
        if self.servo2:
            self.servo2.angle = 180 - angle


class PivotController:
    def __init__(self, servo_pin, debug=False):
        self.debug = debug
        self.servo = None
        if self.debug:
            return

        try:
            from gpiozero import AngularServo
        except Exception as e:
            raise ImportError(f"gpiozero AngularServo not available: {e}")

        self.servo = AngularServo(
            servo_pin,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0009,
            max_pulse_width=0.0021,
        )

    def set_angle(self, angle):
        if self.debug:
            print(f"[debug] PivotController.set_angle({angle})")
            return
        if self.servo:
            self.servo.angle = angle


def _load_positions_file(path=None):
    """Load positions from TrashPositions.txt. Returns dict.

    If path is None, resolve package-relative path.
    """
    if path is None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'settings', 'TrashPositions.txt'))

    positions = {}
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                try:
                    positions[key.strip()] = int(value.strip())
                except ValueError:
                    print(f"Warning: invalid integer for position {key} in {path}: {value}")
    except FileNotFoundError:
        print(f"Positions file not found: {path}")
    except Exception as e:
        print(f"Failed to read positions file {path}: {e}")

    return positions


class TrashController:
    def __init__(self, arm_servo1, arm_servo2, pivot_servo, debug=False, positions=None):
        self.debug = debug
        # Load positions lazily or use provided positions dict (for testing)
        self.positions = positions or _load_positions_file()

        if self.debug:
            print("Debug mode: servos will not be moved.")
            # do not initialize hardware in debug mode
            self.arm = None
            self.pivot = None
            return

        print(f"Initializing TrashController with arm servos on GPIO {arm_servo1} and {arm_servo2}, pivot servo on GPIO {pivot_servo}")
        self.arm = ArmController(arm_servo1, arm_servo2, debug=self.debug)
        self.pivot = PivotController(pivot_servo, debug=self.debug)

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
        self.arm.set_angle(self.positions.get('arm_pos', 90))
        self.pivot.set_angle(self.positions.get('pivot_pos', 50))

    def move_front_left(self):
        print("Moving to front left...")
        if self.debug:
            print("Debug mode: skipping actual servo movement.")
            return
        self.arm.set_angle(self.positions.get('arm_rev_pos', 90))
        self.pivot.set_angle(self.positions.get('pivot_pos', 50))

    def move_back_left(self):
        print("Moving to back left...")
        if self.debug:
            print("Debug mode: skipping actual servo movement.")
            return
        self.arm.set_angle(self.positions.get('arm_pos', 90))
        self.pivot.set_angle(self.positions.get('pivot_rev_pos', 50))

    def move_front_right(self):
        print("Moving to front right...")
        if self.debug:
            print("Debug mode: skipping actual servo movement.")
            return
        self.arm.set_angle(self.positions.get('arm_rev_pos', 90))
        self.pivot.set_angle(self.positions.get('pivot_rev_pos', 50))
