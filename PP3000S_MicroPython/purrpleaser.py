import time
from machine import Pin
import network
from umqtt.simple import MQTTClient

from config import *
from credentials import *
from stepper import Stepper
from hx711 import HX711
from schedule import Schedule

class PurrPleaser:
    def __init__(self):
        self.led = Pin(LED_PIN, Pin.OUT)
        self.stepper = Stepper(MOTOR_STEP_PIN_1, MOTOR_DIR_PIN_1)
        self.scale = HX711(SCALE_DATA_PIN_1, SCALE_CLOCK_PIN_1)
        self.schedule = Schedule()
        self.mqtt = None

    def connect_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep_ms(500)
        return wlan.ifconfig()[0]

    def connect_mqtt(self):
        client_id = PP_NAME.replace(' ', '_')
        self.mqtt = MQTTClient(client_id, MQTT_BROKER, port=MQTT_PORT,
                               user=MQTT_USER, password=MQTT_PASSWORD)
        self.mqtt.connect()

    def feed(self, grams):
        self.led.high()
        self.scale.tare()
        steps = int(grams * 100)  # TODO: calibrate
        self.stepper.move_steps(steps)
        weight = self.scale.read()
        self.led.low()
        if self.mqtt:
            self.mqtt.publish("purrpleaser/last_feed", str(weight))

    def run(self):
        self.connect_wifi()
        try:
            self.connect_mqtt()
        except Exception:
            pass
        while True:
            if self.schedule.should_feed():
                self.feed(TREAT_AMOUNT)
            time.sleep(1)
