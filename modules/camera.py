from servosix import ServoSix

ss = ServoSix()

class Camera():
    cam = {'x': 80, 'y': 60}

    def __init__(self):
        self.move(self.cam['x'], self.cam['y'])

    def __exit__(self):
        ss.cleanup()

    def move(self, x, y):
        # Only move if the new x request is different from the current cam['x'] angle
        if x != self.cam['x']:
            self.pan_tilt('x', x, '')

        if y != self.cam['y']:
            self.pan_tilt('y', y, '')

    # Default is to move left/right or up/down 10 degrees ('step' type)
    # Pass 'snap' as a type to move to the extreme of that axis (for example 'x', 'forwards', 'snap')
    # Pass an integer as the second parameter to move directly to that degree - the third parameter is then ignored (e.g. 'x', 100, '')
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

            print axis, direction, self.cam[axis]

            servo = 1 if axis == 'x' else 2
            ss.set_servo(servo, self.cam[axis])
    #        percent = (cam[axis] / 180) * 100
    #        os.system("echo {}={}% > /dev/servoblaster".format(servo, percent))
        return True
