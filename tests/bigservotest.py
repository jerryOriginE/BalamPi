from gpiozero import Servo
from time import sleep

#servo = Servo(
#    6,
#    min_pulse_width=0.0005,  # 0.5 ms
#    max_pulse_width=0.0025   # 2.5 ms
#)
#
#while True:
#
#    for pos in [-1, -0.5, 0, 0.5, 1]:
#        print(f"Position: {pos}")
#        servo.value = pos
#        sleep(2)

class BigServo():
    def __init__(self, pin, min_pulse_width=0.0005, max_pulse_width=0.0025, inverted=False):
        self.pin = pin
        self.min_pulse_width = min_pulse_width
        self.max_pulse_width = max_pulse_width
        self.inverted = inverted

        self.servo = Servo(
            self.pin,
            min_pulse_width=self.min_pulse_width,
            max_pulse_width=self.max_pulse_width
        )
        print(f"Initialized servo on pin {self.pin} with pulse widths {self.min_pulse_width} to {self.max_pulse_width}")

    def set_angle(self, position):
        if position < -1 or position > 1:
            raise ValueError("Position must be between -1 and 1")
        
        if self.inverted:
            position = -position
        else:
            self.servo.value = position

    def detach(self):
        self.servo.detach()


class Controller():
    def __init__(self, servo, servo2, servo1_inverted=False, servo2_inverted=False):
        self.servo = BigServo(servo, inverted=servo1_inverted)
        self.servo2 = BigServo(servo2, inverted=servo2_inverted)

    def stop_servos(self):
        self.servo.detach()
        self.servo2.detach()

    def move_servos(self, position):
        self.servo.set_angle(position)
        self.servo2.set_angle(-position)

        sleep(1)
        self.stop_servos()


def main():
    controller = Controller(5, 6, False, False)

    #controller.move_servos(-1)

    while True:
        for pos in [-1, 0]:
            print(f"Moving to position: {pos}")
            controller.move_servos(pos)
            sleep(2)

if __name__ == "__main__":    main()