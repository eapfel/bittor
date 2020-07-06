import os
from pathlib import Path
import yaml

from src.main.python.utils.utils import base_dir


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):

    def __init__(self):

        config_file = base_dir() / 'src' / 'main' / 'resources' / 'config.yml'

        # path = os.path.dirname(os.path.abspath('../../resources/config.yml')) if os.path.abspath(
        #     '../resources/config.yml').__contains__('test') else os.path.dirname(
        #     os.path.abspath('../resources/config.yml'))

        with open(config_file, "r") as ymlfile:
            self.config = yaml.load(ymlfile)

    def get(self, key):
        return self.config.get(key)
