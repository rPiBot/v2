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
sensors.daemon = True
sensors.start()

try:
    while True:
        time.sleep(0.05)
        Config.read_config(config)      # Keep reading config for changes

        Body.move(body, Config.retrieve(config, 'Body', 'direction'), Sensors.retrieve(sensors), config)
        Camera.move(camera, Config.retrieve(config, 'Head', 'x'), Config.retrieve(config, 'Head', 'y'))

except KeyboardInterrupt:
    Sensors.__exit__(sensors)
    Body.__exit__(body)
    Camera.__exit__(camera)
    Config.__exit__(config)
    exit()
