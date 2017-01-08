from modules.config import Config
import RPi.GPIO as GPIO
import time

class Sensors:
    sensors = { 'F': 0, 'R': 0}

    def __init__(self, config):
        GPIO.setmode(GPIO.BOARD)
        TRIG = { 'F': 33, 'R': 31}
        ECHO = { 'F': 40, 'R': 32}

        GPIO.setup(TRIG['F'], GPIO.OUT)
        GPIO.setup(TRIG['R'], GPIO.OUT)
        GPIO.setup(ECHO['F'], GPIO.IN)
        GPIO.setup(ECHO['R'], GPIO.IN)

        while True:
            self.sensors['F'] = self.check_distance(self, TRIG['F'], ECHO['F'])
            self.sensors['R'] = self.check_distance(self, TRIG['R'], ECHO['R'])

            time.sleep(0.05)

    def retrieve(self):
        return self.sensors

    def check_distance(self, trigger, echo):
        time.sleep(0.005) # Wait for sensor to be ready
        GPIO.output(trigger, True)
        time.sleep(0.00001)
        GPIO.output(trigger, False)

        while GPIO.input(echo) == 0:
            start = time.time()

        while GPIO.input(echo) == 1:
            end = time.time()

        duration = end - start
        return round((duration * 17150), 2)
