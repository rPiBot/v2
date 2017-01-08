import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

class Body:
    state = ''

    def move(self, direction, sensors):
        if direction != self.state:
            GPIO.output(35, False)
            GPIO.output(36, False)
            GPIO.output(37, False)
            GPIO.output(38, False)

            GPIO.output(TRIG_FRONT, False)
            GPIO.output(TRIG_REAR, False)

            self.state = direction

            print 'checking distance'

            if direction == 'forwards':
                while sensors['F'] > 20: # AND state == forwards FROM CONFIG FILE
                  GPIO.output(37, True)
                  GPIO.output(38, True)
                else:
                  print 'Not safe to drive forwards'
                  GPIO.output(37, False)
                  GPIO.output(38, False)
            elif direction == 'backwards':
                while sensors['R'] > 20: # AND state == backwards FROM CONFIG FILE
                    GPIO.output(35, True)
                    GPIO.output(36, True)
                else:
                    print 'Not safe to drive backwards'
                    GPIO.output(35, False)
                    GPIO.output(36, False)
            elif direction == 'right':
                GPIO.output(38, True)
                GPIO.output(35, True)
            elif direction == 'left':
                GPIO.output(36, True)
                GPIO.output(37, True)

            print direction
