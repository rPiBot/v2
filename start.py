import os, sys, time
from datetime import datetime

from modules.camera import Camera
from modules.body import Body
from modules.config import Config
from modules.sensors import Sensors

body = Body()
camera = Camera('')
config = Config()
sensors = Sensors(config)

while True:
    time.sleep(0.01)
    Config.read_config(config)      # Keep reading config for changes

    if (Config.retrieve(config, 'Body', 'status') == 'moving'):
        direction = Config.retrieve(config, 'Body', 'direction')
        sensors = { 'F': Config.retrieve(config, 'Sensors', 'F'), 'R': Config.retrieve(config, 'Sensors', 'R') }

        Body.move(body, direction, sensors)
    else:
        Body.stop(body)

    # only if different from current:
    #Camera.pan_tilt(camera, 'x', Config.retrieve('Camera', 'x'), 'step')
    #Camera.pan_tilt(camera, 'y', Config.retrieve('Camera', 'y'), 'step')
