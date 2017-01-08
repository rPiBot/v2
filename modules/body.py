import RPi.GPIO as GPIO
import time, random

GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

class Body:
    state = ''

    def move(self, direction, sensors):
        if (direction == 'forwards' and sensors['F'] < 20) or (direction == 'backwards' and sensors['R'] < 20):
            print "Not safe to drive", direction
            direction = 'STOPPED - was unsafe'

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

        if direction != self.state:
            GPIO.output(35, False)
            GPIO.output(36, False)
            GPIO.output(37, False)
            GPIO.output(38, False)

            self.state = direction

            print 'checking distance'

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
                GPIO.output(35, False)
                GPIO.output(36, False)
                GPIO.output(37, False)
                GPIO.output(38, False)
                self.state = 'stopped after evading'

            print direction
