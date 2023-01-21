import asyncio
import json
import logging
import socket
from dataclasses import dataclass
from time import sleep

from board import BoardDistributed
from rich import print
from service import MonitoringServices
from utils import read_config_board

# art = """\
#     ______ ____  _____             ____ ____  ___    ____
#    / ____/ ___// ____/           / ___// __ \/   |  / __ \
#   / /_   \__ \/ __/    ______    \__ \/ / / / /| | / /_/ /
#  / __/  ___/ / /___   /_____/   ___/ / /_/ / ___ |/ ____/
# /_/    /____/_____/            /____/_____/_/  |_/_/
#
# Sistema Distribuído de Automação Predial
# """


@dataclass
class DistributedServer:

    board: BoardDistributed
    service: MonitoringServices

    def __post_init__(self):
        self.board.setup_mode_gpio
        self.board.setup_devices_turn_off()
        self.board.setup_sensors()
        print("#--#" * 60)
        print(self.board)
        print("#--#" * 60)
        print(self.service)
        print("#--#" * 60)

#     def receive_command(self):
#         pass

#     def control_alarm_sensors(self):
#         self.service.read_motion_sensor()
#         self.service.read_windom_sensor()
#         self.service.read_smoke_detector()
#         self.service.read_door_sensor()

#     def control_ocupancy(self):
#         self.service.read_people_in_sensor()    # ocupancy+=1
#         self.service.read_people_out_sensor()
    
#     def control_temperature_humidity(self):
#         def read_dht22()

#     def turn_on_15seg_lamps_turn_off:
# #     # sleep(15)
# #     # GPIO.output([pinos[l]["GPIO"] for l in luzes], 0)
# #     pass
    
    def parser_csv(self, data):
        if data:
            data = json.loads(data)
            print(data)
            
            data = data.decode('utf-8')
            data = json.loads(data)
            return data
            
            # player.decide_play_alarm(data['activate_alarm'])
            # menu.show_data(data)
            # csv_obj.write_row(data)
    
    
    def listen_sensor_udp(self):
        print("Listener udp")
        print(f"udp_ip = {self.board.ip_server}")
        print(f"udp_port= {self.board.port_server}")
        
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        udp_socket.bind((self.board.ip_server, self.board.port_server))
        
        while True:
            data, addr = udp_socket.recvfrom(1024)
            data = self.parser_csv(data)
            yield data, addr



    def send_comand_data(self):
        UDP_IP =  self.board.ip_server
        UDP_PORT = self.board.port_server
        
        print("send command")
        print(f"udp_ip = {self.board.ip_server} - {UDP_IP}")
        print(f"udp_port= {self.board.port_server} - {UDP_PORT} ")
        
        print("*-*" * 45)
        config_data = read_config_board("config_board.json", "rasp42")
        print("Mensagem Dicionairo:")
        print(f"{config_data}")
        print("*-*" * 45)
        print("Mensagem Json:")
        mensage = json.dumps(config_data).encode('utf-8')
        print(mensage)
        print("*-*" * 45)
        
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        received = False
        while not received:
            print("Enviando json!!")
            num_bytes = udp_socket.sendto(mensage, (self.board.ip_server, int(self.board.port_server)))
            # num_bytes = udp_socket.sendto(mensage, (UDP_IP, UDP_PORT))
            print(f"Numero de bytes enviado: {num_bytes}")
            
            print("Aguardando recebido:")
            data, addr = udp_socket.recvfrom(1024) 
            
            print(f"data raw: {data}")
            print(f"type: {type(data)}")
            data = bool(data.decode())
            print(f"data dec: {data}")
            print(f"type: {type(data)}")
            print(f"rescponse server: {addr}")

            received = data

            sleep(5)


        # def run():
        #     pass

        # def stop():
        #     pass


def main():
    board = BoardDistributed()
    serv = MonitoringServices(board)
    ds = DistributedServer(board, serv)

    ds.listen_sensor_udp()
    ds.send_comand_data()


if __name__ == "__main__":
    main()
