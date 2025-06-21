import time
from machine import Pin
import network
from umqtt.simple import MQTTClient
import ujson

from config import *
from credentials import *
from stepper import Stepper
from hx711 import HX711
from schedule import Schedule

class PurrPleaser:
    def __init__(self):
        self.led = Pin(LED_PIN, Pin.OUT)
        self.stepper = Stepper(MOTOR_STEP_PIN_1, MOTOR_DIR_PIN_1, limit_pin=LIMIT_SWITCH_1)
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
        self.mqtt.set_callback(self.on_message)
        self.mqtt.connect()
        self.mqtt.subscribe(b"purrpleaser/feed")
        self.mqtt.subscribe(b"purrpleaser/tare")
        self.mqtt.subscribe(b"purrpleaser/calibrate")
        self.mqtt.subscribe(b"purrpleaser/schedule/set")

    def feed(self, grams):
        self.led.high()
        self.scale.tare()
        fed = 0.0
        while fed < grams:
            self.stepper.move_steps(50)
            time.sleep(0.1)
            fed = self.scale.read()
            if fed >= grams or fed >= MAX_SINGLE:
                break
        self.stepper.disable()
        self.led.low()
        if self.mqtt:
            self.mqtt.publish(b"purrpleaser/last_feed", str(fed))

    def on_message(self, topic, msg):
        if topic == b"purrpleaser/feed":
            try:
                grams = float(msg)
            except ValueError:
                grams = TREAT_AMOUNT
            self.feed(grams)
        elif topic == b"purrpleaser/tare":
            self.scale.tare()
        elif topic == b"purrpleaser/calibrate":
            try:
                weight = float(msg)
                self.scale.calibrate(weight)
            except ValueError:
                pass
        elif topic == b"purrpleaser/schedule/set":
            try:
                data = ujson.loads(msg)
                idx = data.get("index", 0)
                if "hour" in data and "minute" in data:
                    self.schedule.set_time(idx, data["hour"], data["minute"])
                if "amount" in data:
                    self.schedule.set_amount(idx, float(data["amount"]))
            except Exception:
                pass

    def run(self):
        self.connect_wifi()
        try:
            self.connect_mqtt()
        except Exception:
            pass
        while True:
            feed, amount = self.schedule.should_feed()
            if feed:
                self.feed(amount)
            if self.mqtt:
                self.mqtt.check_msg()
            time.sleep(1)
