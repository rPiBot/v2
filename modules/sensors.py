from modules.config import Config
import RPi.GPIO as GPIO
import time

class Sensors:
    def __init__(self, config):
        GPIO.setmode(GPIO.BOARD)
        TRIG = { 'F': 33, 'R': 31}
        ECHO = { 'F', 40, 'R', 32}

        GPIO.setup(TRIG['F'], GPIO.OUT)
        GPIO.setup(TRIG['R'], GPIO.OUT)
        GPIO.setup(ECHO['F'], GPIO.IN)
        GPIO.setup(ECHO['R'], GPIO.IN)

        while True:
            Config.update_config(config, 'Sensors', 'F', check_distance(self, TRIG['F'], ECHO['F']))
            Config.update_config(config, 'Sensors', 'R', check_distance(self, TRIG['R'], ECHO['R']))
            time.sleep(0.05)

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
