import os, sys, time
from datetime import datetime
import threading

from modules.camera import Camera
from modules.body import Body
from modules.config import Config
from modules.sensors import Sensors

body = Body()
camera = Camera()
config = Config()

sensors = Sensors()
sensors.start()

try:
    while True:
        time.sleep(0.02)
        Config.read_config(config)      # Keep reading config for changes

        u_sensors = Sensors.retrieve(sensors)

        Body.move(body, Config.retrieve(config, 'Body', 'direction'), u_sensors, config)
        Camera.move(camera, Config.retrieve(config, 'Head', 'x'), Config.retrieve(config, 'Head', 'y'))

except KeyboardInterrupt:
    return False
