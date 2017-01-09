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
        if (direction == 'forwards' and sensors['F'] < 20) or (direction == 'backwards' and sensors['R'] < 20):
            print "Not safe to drive", direction
            direction = 'stopped (unsafe)'

        auto_stop = False

        if sensors['F'] < 10:
            direction = 'backwards'
            auto_stop = True

        if sensors['R'] < 10:
            direction = 'forwards'
            auto_stop = True

        if sensors['F'] < 10 and sensors['R'] < 10:
            direction = random.choice(['left', 'right'])
            auto_stop = True

        Config.update_config(config, 'Body', 'direction', direction)

        if direction != self.state:
            GPIO.output(35, False)
            GPIO.output(36, False)
            GPIO.output(37, False)
            GPIO.output(38, False)

            self.state = direction

            if direction == 'forwards':
              GPIO.output(37, True)
              GPIO.output(38, True)
            elif direction == 'backwards':
              GPIO.output(35, True)
              GPIO.output(36, True)
            elif direction == 'left':
                GPIO.output(36, True)
                GPIO.output(37, True)
            elif direction == 'right':
                GPIO.output(38, True)
                GPIO.output(35, True)

            # Evade mode - move in a direction for only half a second based on sensor information
            if auto_stop == True:
                time.sleep(0.5)
                self.stop(config)

            print direction
