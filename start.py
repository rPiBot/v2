import os, sys, time
from datetime import datetime

from modules.camera import Camera
from modules.body import Body
from modules.config import Config
from modules.sensors import Sensors

body = Body()
camera = Camera()
config = Config()
sensors = Sensors(config)

while True:
    time.sleep(0.01)
    Config.read_config(config)      # Keep reading config for changes

    sensors = Sensors.retrieve(sensors)
    print sensors   #TODO check they're updating
    Body.move(body, direction, sensors, config)
    Camera.move(camera, Config.retrieve(config, 'Camera', 'x'), Config.retrieve(config, 'Camera', 'y'))

    # only if different from current:
    #Camera.pan_tilt(camera, 'x', Config.retrieve('Camera', 'x'), 'step')
    #Camera.pan_tilt(camera, 'y', Config.retrieve('Camera', 'y'), 'step')
