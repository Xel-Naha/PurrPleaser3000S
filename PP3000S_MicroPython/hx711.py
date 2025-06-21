from machine import Pin
import time

class HX711:
    def __init__(self, data_pin, clock_pin, gain=128):
        self.data = Pin(data_pin, Pin.IN, pull=Pin.PULL_UP)
        self.clock = Pin(clock_pin, Pin.OUT)
        self.gain = gain
        self.offset = 0
        self.scale = 1
        self.power_on()

    def power_on(self):
        self.clock.low()
        time.sleep_ms(100)

    def is_ready(self):
        return self.data.value() == 0

    def read_raw(self):
        while not self.is_ready():
            time.sleep_ms(1)
        value = 0
        for _ in range(24):
            self.clock.high()
            value = (value << 1) | self.data.value()
            self.clock.low()
        for _ in range({128:1,64:3,32:2}[self.gain]):
            self.clock.high()
            self.clock.low()
        if value & 0x800000:
            value -= 0x1000000
        return value

    def read(self):
        return (self.read_raw() - self.offset) / self.scale

    def tare(self, samples=10):
        total = sum(self.read_raw() for _ in range(samples))
        self.offset = total / samples

    def calibrate(self, known_weight):
        self.tare()
        reading = self.read_raw()
        self.scale = (reading - self.offset) / known_weight
