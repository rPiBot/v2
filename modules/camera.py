from servosix import ServoSix

ss = ServoSix()

class Camera():
    cam = {'x': 80, 'y': 60}
    state = ''

    def __init__(self, initial_state):
        if initial_state != 'reset':
            self.pan_tilt('x', 'reset', 0)
            self.pan_tilt('y', 'reset', 0)
            self.state = 'reset'

    def __exit__(self):
        ss.cleanup()

    def pan_tilt(self, axis, direction, type):
        defaults = { 'size': 10, 'range_min': 20, 'range_max': 160, 'x': 80, 'y': 60 }

        if (self.cam[axis] <= defaults['range_min'] and direction == 'negative') or (self.cam[axis] >= defaults['range_max'] and direction == 'positive'):
            return False

        else:
            if direction == 'positive':
                self.cam[axis] = self.cam[axis] + defaults['size'] if type == 'step' else defaults['range_max']
            elif direction == 'negative':
                self.cam[axis] = self.cam[axis] - defaults['size'] if type == 'step' else defaults['range_min']
            elif direction == 'reset':
                self.cam[axis] = defaults[axis]
            else:
                self.cam[axis] = float(direction)

            self.state = direction

            print axis, direction, self.cam[axis]

            servo = 1 if axis == 'x' else 2
            ss.set_servo(servo, self.cam[axis])
    #        percent = (cam[axis] / 180) * 100
    #        os.system("echo {}={}% > /dev/servoblaster".format(servo, percent))
        return True
