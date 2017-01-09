from modules.config import Config
import RPi.GPIO as GPIO
import time, threading

class Sensors(threading.Thread):
    sensors = { 'F': 0, 'R': 0}
    running = True

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        GPIO.setmode(GPIO.BOARD)
        TRIG = { 'F': 33, 'R': 31}
        ECHO = { 'F': 40, 'R': 32}

        GPIO.setup(TRIG['F'], GPIO.OUT)
        GPIO.setup(TRIG['R'], GPIO.OUT)
        GPIO.setup(ECHO['F'], GPIO.IN)
        GPIO.setup(ECHO['R'], GPIO.IN)

        while True and self.running:
            self.sensors['F'] = self.check_distance(TRIG['F'], ECHO['F'])
            self.sensors['R'] = self.check_distance(TRIG['R'], ECHO['R'])

            time.sleep(0.1)

    def stop(self):
        self.running = False

    def __exit__(self):
        self.stop()
        GPIO.cleanup()

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
