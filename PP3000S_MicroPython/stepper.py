from machine import Pin
import time

class Stepper:
    def __init__(self, step_pin, dir_pin, enable_pin=None, limit_pin=None):
        self.step = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)
        self.enable = Pin(enable_pin, Pin.OUT) if enable_pin is not None else None
        self.limit = Pin(limit_pin, Pin.IN, Pin.PULL_UP) if limit_pin is not None else None
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
            if self.limit and self.limit.value() == 0:
                break

    def disable(self):
        if self.enable:
            self.enable.high()

    def home(self, direction=-1, speed=1000, max_steps=10000):
        if not self.limit:
            return
        self.dir.value(1 if direction > 0 else 0)
        for _ in range(max_steps):
            if self.limit.value() == 0:
                break
            self.step.high()
            time.sleep(0.5 / speed)
            self.step.low()
            time.sleep(0.5 / speed)
