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
        if ((direction == 'forwards' or self.state == 'forwards') and sensors['F'] < 25) or ((direction == 'backwards' or self.state == 'backwards') and sensors['R'] < 25):
            print "Not safe to drive", direction
            direction = 'stopped'

        auto_stop = False
        
        if self.state == 'evading':
            self.state = 'stopped'

        if self.state == 'stopped': # Evade if necessary
            if sensors['F'] < 10:
                direction = 'backwards'
                auto_stop = 0.09

            if sensors['R'] < 10:
                direction = 'forwards'
                auto_stop = 0.09

            if sensors['F'] < 10 and sensors['R'] < 10:
                direction = random.choice(['left', 'right'])
                auto_stop = 0.4

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
            else: # stop
                GPIO.output(35, False)
                GPIO.output(36, False)
                GPIO.output(37, False)
                GPIO.output(38, False)

            # Evade mode - move in the direction given for only half a second based on sensor information
            if auto_stop != False:
                #time.sleep(auto_stop)
                #self.stop(config)
                self.state = 'evading'

            print direction
