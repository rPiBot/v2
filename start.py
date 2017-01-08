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

while True:
    time.sleep(0.01)
    Config.read_config(config)      # Keep reading config for changes

    sensors = thread.start_new_thread(Sensors.retrieve(sensors), ())
    print sensors   #TODO check they're updating
    Body.move(body, direction, sensors, config)
    Camera.move(camera, Config.retrieve(config, 'Camera', 'x'), Config.retrieve(config, 'Camera', 'y'))
