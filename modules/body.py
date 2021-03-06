import RPi.GPIO as GPIO
from modules.config import Config
import time, random

GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

class Body:
    state = ''

    def __exit__(self):
        GPIO.cleanup()

    def __init__(self):
        GPIO.output(35, False)
        GPIO.output(36, False)
        GPIO.output(37, False)
        GPIO.output(38, False)

    def stop(self, config):
        if self.state != 'stopped':
            GPIO.output(35, False)
            GPIO.output(36, False)
            GPIO.output(37, False)
            GPIO.output(38, False)
            self.state = 'stopped'
            Config.update_config(config, 'Body', 'direction', 'stopped')

    def move(self, direction, sensors, config):
        if self.state == 'evading':
            direction = 'stopped'

        allowed = { 'F': True, 'R': True }

        if sensors['F'] < 25:
            print 'Not allowed to drive forwards'
            allowed['F'] = False

        if sensors['R'] < 25:
            print 'Not allowed to drive backwards'
            allowed['R'] = False

        if sensors['F'] < 25 or sensors['R'] < 25:
            direction = 'stopped'

        if sensors['F'] < 10:
            direction = 'backwards'

        if sensors['R'] < 10:
            direction = 'forwards'

        if sensors['F'] < 10 and sensors['R'] < 10:
            direction = random.choice(['left', 'right'])

        if sensors['F'] < 10 or sensors['R'] < 10:
            self.state = 'evading'
            print 'Evading', direction

        if direction != self.state:
            if self.state != 'evading':
                self.state = direction

            Config.update_config(config, 'Body', 'direction', direction)

            if direction == 'forwards' and allowed['F']:
                GPIO.output(35, False)
                GPIO.output(36, False)
                GPIO.output(37, True)
                GPIO.output(38, True)
            elif direction == 'backwards' and allowed['R']:
                GPIO.output(35, True)
                GPIO.output(36, True)
                GPIO.output(37, False)
                GPIO.output(38, False)
            elif direction == 'left':
                GPIO.output(35, False)
                GPIO.output(36, True)
                GPIO.output(37, True)
                GPIO.output(38, False)
            elif direction == 'right':
                GPIO.output(35, True)
                GPIO.output(36, False)
                GPIO.output(37, False)
                GPIO.output(38, True)
            else:
                self.stop(config)

            print direction
