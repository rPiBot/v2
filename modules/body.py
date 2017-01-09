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
        print 'stop'
        GPIO.output(35, False)
        GPIO.output(36, False)
        GPIO.output(37, False)
        GPIO.output(38, False)
        self.state = 'stopped'
        Config.update_config(config, 'Body', 'direction', 'stopped')

    def move(self, direction, sensors, config):
        if self.state == 'evading':
            direction = 'stop'
            self.state = 'stopping'

        if (sensors['F'] < 25 or sensors['R'] < 25):
            if sensors['F'] < 10:
                direction = 'backwards'
                self.state = 'evading'
            elif sensors['R'] < 10:
                direction = 'forwards'
                self.state = 'evading'
            elif sensors['F'] < 10 and sensors['R'] < 10:
                direction = random.choice(['left', 'right'])
                self.state = 'evading'
            else:
                print 'stopping here'
                self.stop(config)

    #    print 'a', self.state
#        print 'a', direction

        if direction != self.state and self.state != 'stopping':
            self.state = direction

            if direction == 'forwards':
                GPIO.output(35, False)
                GPIO.output(36, False)
                GPIO.output(37, True)
                GPIO.output(38, True)
                Config.update_config(config, 'Body', 'direction', direction)

            elif direction == 'backwards':
                GPIO.output(35, True)
                GPIO.output(36, True)
                GPIO.output(37, False)
                GPIO.output(38, False)
                Config.update_config(config, 'Body', 'direction', direction)

            elif direction == 'left':
                GPIO.output(35, False)
                GPIO.output(36, True)
                GPIO.output(37, True)
                GPIO.output(38, False)
                Config.update_config(config, 'Body', 'direction', direction)

            elif direction == 'right':
                GPIO.output(35, True)
                GPIO.output(36, False)
                GPIO.output(37, False)
                GPIO.output(38, True)
                Config.update_config(config, 'Body', 'direction', direction)

            else:
                print 'this stop'
                self.stop(config)

            print 'moved', direction
