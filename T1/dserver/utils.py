import csv
import json
import sys
from enum import Enum

CONFIG_GPIO = "config_gpio.json"
CONFIG_BOARD = "config_board.json"
ON = True
OFF = False
LIGHT_BLULB_01 = "LB1"
LIGHT_BLULB_02 = "LB2"
MULTIMEDIA_PROJECTOR = "MP"
AIR_CONDITIONER = "AC"
SIRENE_ALARME = '"SA"'
MOTION_SENSOR = "MS"
SMOKE_DETECTOR = "SD"
WINDOW_SENSOR = "WS"
DOOR_SENSOR = "DS"
PEOPLE_IN_SENSOR = "PIS"
PEOPLE_OUT_SENSOR = "POS"
TEMPERATURE_HUMIDITY_SENSOR = "THS"


# class Pin(Enum):
#     ON = True
#     OFF = False

# class Tag(Enum):
#     LB1 = "light_blulb_01"
#     LB2 = "light_blulb_02"
#     MP = "multimedia_projector"
#     AC = "air_conditioner"
#     SA = "sirene_alarme"
#     MS = "motion_sensor"
#     SD = "smoke_detector"
#     WS = "window_sensor"
#     DS = "door_sensor"
#     PIS = "people_in_sensor"
#     POS = "people_out_sensor"
#     THS = "temperature_humidity_sensor"


class Config(object):
    def __init__(self, adict=None):
        if adict:
            self.__dict__.update(adict)

    def __str__(self):
        config_dict = vars(self)
        return json.dumps(config_dict, indent=4)

    @classmethod
    def load(cls, fname):
        self = cls()
        with open(fname) as f:
            data = json.load(f)
        for k, v in data.items():
            setattr(self, k, v)
        return self

    def save(self, fname):
        config_dict = vars(self)
        with open(fname, "w") as f:
            json.dump(config_dict, f, indent=4)


conf = Config().load(CONFIG_GPIO)


def read_config_gpio(config_file: str, dir: str):
    with open(config_file) as file:
        data = json.load(file)
        return {key: value for key, value in data.items() if value.get("dir") == dir}


def read_config_board(config_file: str, board: str):
    with open(config_file) as file:
        data = json.load(file)
        return data.get(board)
