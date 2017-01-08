import ConfigParser, time
from datetime import datetime

class Config:

    config_file = 'config.ini'
    config = ConfigParser.ConfigParser()

    def __init__(self):
        self.config.add_section('Mode')
        self.config.set('Mode', 'control', 'manual')

        self.config.add_section('Head')
        self.config.set('Head', 'x', 90)
        self.config.set('Head', 'y', 90)

        self.config.add_section('Body')
        self.config.set('Body', 'status', 'stopped')
        self.config.set('Body', 'direction')

        self.config.add_section('Sensors')
        self.config.set('Sensors', 'F', 0)
        self.config.set('Sensors', 'R', 0)

        self.config.add_section('System')
        self.config.set('System', 'created', str(datetime.now()))
        self.config.set('System', 'updated', str(datetime.now()))
        self.write_config()

    def update_config(self, section, key, value):
        self.config.read(self.config_file)
        self.config.set(section, key, value)
        self.config.set('System', 'updated', str(datetime.now()))
        self.write_config()

    def read_config(self):
        self.config.read(self.config_file)

    def retrieve(self, section, key):
        return self.config.get(section, key)

    def write_config(self):
        with open(self.config_file, 'w') as configfile:
          self.config.write(configfile)
