from machine import Pin
import time

class Stepper:
    def __init__(self, step_pin, dir_pin, enable_pin=None):
        self.step = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)
        self.enable = Pin(enable_pin, Pin.OUT) if enable_pin is not None else None
        if self.enable:
            self.enable.low()

    def move_steps(self, steps, speed=1000):
        delay = 1.0 / speed
        direction = 1 if steps > 0 else 0
        self.dir.value(direction)
        for _ in range(abs(steps)):
            self.step.high()
            time.sleep(delay/2)
            self.step.low()
            time.sleep(delay/2)

    def disable(self):
        if self.enable:
            self.enable.high()
