from dataclasses import dataclass
from time import sleep

from board import BoardDistributed
from rich import print
from utils import (AIR_CONDITIONER, DOOR_SENSOR, LIGHT_BLULB_01,
                   LIGHT_BLULB_02, MOTION_SENSOR, MULTIMEDIA_PROJECTOR, OFF,
                   ON, PEOPLE_IN_SENSOR, PEOPLE_OUT_SENSOR, SIRENE_ALARME,
                   SMOKE_DETECTOR, TEMPERATURE_HUMIDITY_SENSOR, WINDOW_SENSOR)


@dataclass
class MonitoringServices:

    board: BoardDistributed
    light_bulb_01: bool = OFF
    light_bulb_02: bool = OFF
    multimedia_projector: bool = OFF
    air_conditioner: bool = OFF
    sirene_alarme: bool = OFF

      
    # --------------------------------------------------------------------

    def get_state_light_bulb_01(self):
        return self.light_bulb_01

    def toggle_on_off_light_bulb_01(self):
        if self.light_bulb_01:
            self.board.turn_off_device(LIGHT_BLULB_01)
        else:
            self.board.turn_on_device(LIGHT_BLULB_01)

    # --------------------------------------------------------------------

    def get_state_light_bulb_02(self):
        return self.light_bulb_02

    def toggle_on_off_light_bulb_02(self):
        if self.light_bulb_02:
            self.board.turn_off_device(LIGHT_BLULB_02)
        else:
            self.board.turn_on_device(LIGHT_BLULB_02)


    # --------------------------------------------------------------------


    def get_state_multimedia_projector(self):
        return self.multimedia_projector


    def toggle_on_off_multimedia_projector(self):
        if self.multimedia_projector:
            self.board.turn_off_device(MULTIMEDIA_PROJECTOR)
        else:
            self.board.turn_on_device(MULTIMEDIA_PROJECTOR)


# --------------------------------------------------------------------


    def get_state_air_conditioner(self):
        return self.air_conditioner


    def toggle_on_off_air_conditioner(self):
        if self.air_conditioner:
            self.board.turn_off_device(AIR_CONDITIONER)
        else:
            self.board.turn_on_device(AIR_CONDITIONER)


# --------------------------------------------------------------------

    def get_state_sirene_alarme(self):
        return self.sirene_alarme


    def toggle_on_off_sirene_alarme(self):
        if self.sirene_alarme:
            self.board.turn_off_device(SIRENE_ALARME)
        else:
            self.board.turn_on_device(SIRENE_ALARME)


# # --------------------------------------------------------------------
#     def read_motion_sensor(self):
#           self.board.read_pin(MOTION_SENSOR)
        
#     def read_windom_sensor(self):
#          self.board.read_pin(WINDOW_SENSOR)
        
#     def read_smoke_detector(self):
#          self.board.read_pin(SMOKE_DETECTOR)
        
#     def read_door_sensor(self):
#              self.board.read_pin(DOOR_SENSOR)
#         #     ligar_sirene
#     # --------------------------------------------------------------------

#     def  read_people_in_sensor(self):PEOPLE_IN_SENSOR
#         self.board.read_pin()
    
#     def  read_people_out_sensor(self):PEOPLE_OUT_SENSOR
#          self.board.read_pin()

#     # --------------------------------------------------------------------

#     def read_dht22(self):TEMPERATURE_HUMIDITY_SENSOR
#         pass
#         # while True:
#     #     sleep(2)

# # # =====================================================


def main():
    board_distributed = BoardDistributed()
    services = MonitoringServices(board_distributed)

    print("- = -" * 40)
    print(board_distributed)
    print("- = -" * 40)
    print(services)
    print("- = -" * 40)

    # print(services.light_bulb_01)
    # print(services.light_bulb_02)
    # print(services.multimedia_projector)
    # print(services.air_conditioner)
    # print(services.light_bulb_01)
    # print(services.sirene_alarme)

    l1 = services.get_state_light_bulb_01()
    l2 = services.get_state_light_bulb_02()
    services.toggle_on_off_light_bulb_01()
    # services.toggle_on_off_light_bulb_02()
    # services.get_state_light_bulb_01()
    # services.get_state_light_bulb_02()

    print(f"Lampada 1 = {l1}")
    print(f"Lampada 2 = {l2}")


if __name__ == "__main__":
    main()

# # =====================================================
