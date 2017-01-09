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

    def stop(self, config):
        GPIO.output(35, False)
        GPIO.output(36, False)
        GPIO.output(37, False)
        GPIO.output(38, False)
        self.state = 'stopped'
        Config.update_config(config, 'Body', 'direction', 'stopped')

    def move(self, direction, sensors, config):
        if (sensors['F'] < 25 or sensors['R'] < 25):
            print "Not safe to drive", direction
            self.state = 'stopped'

        if self.state == 'evading':
            direction = 'stopped'
            self.state = 'stopped'

        if self.state == 'stopped': # Evade if necessary
            if sensors['F'] < 10:
                direction = 'backwards'
                self.state = 'evading'

            if sensors['R'] < 10:
                direction = 'forwards'
                self.state = 'evading'

            if sensors['F'] < 10 and sensors['R'] < 10:
                direction = random.choice(['left', 'right'])
                self.state = 'evading'

        if self.state == 'stopped' or direction == 'stopped':
            self.stop(config)

        if direction != self.state:
            Config.update_config(config, 'Body', 'direction', direction)
            self.state = direction

            if direction == 'forwards':
                GPIO.output(35, False)
                GPIO.output(36, False)
                GPIO.output(37, True)
                GPIO.output(38, True)
            elif direction == 'backwards':
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
