import socket
import sys
import textwrap
from abc import ABC
from dataclasses import asdict, dataclass, field
from json import dumps

from rich import print
from utils import read_config_board, read_config_gpio

# import RPi.GPIO as GPIO

CONFIG_GPIO = "config_gpio.json"
CONFIG_BOARD = "config_board.json"


@dataclass
class BoardCentral(ABC):

    board: str = field(init=False)
    room: str = field(init=False)
    ip: str = field(init=False)
    ip_server: str = field(init=False)
    port_server: str = field(init=False)
    type: str = field(init=False)

    def __post_init__(self):
        self.board = socket.gethostname()
        self.ip = socket.gethostbyname(self.board)
        self._load_config_board(CONFIG_BOARD)

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json_object(self):
        return dumps(self.__dict__)
    
    def create_json(self, name_file: str):
        try:
            with open(name_file, "w") as outfile:
                outfile.write(self.json_object)
        except Exception as e:
            print(f"Erro na criação do arquivo json. {e}")
            
        print(f"{name_file} criado com sucesso!")


    def _load_config_board(self, config_file: str):
        try:
            config_data = read_config_board(config_file, self.board)
        
        except Exception as e:
            print(f"Erro na leitura arquivo json. {e}")
            sys.exit()

        self.board = config_data.get("board")
        self.room = config_data.get("room")
        self.ip_server = config_data.get("ip_server")
        self.port_server = config_data.get("port_server")
        self.type = config_data.get("type")


@dataclass
class BoardDistributed(BoardCentral):

    inputs: dict[str, dict[str, str]] = field(default_factory=dict)
    outputs: dict[str, dict[str, str]] = field(default_factory=dict)
    onewire: dict[str, dict[str, str]] = field(default_factory=dict)
    # states: dict[str, str] = field(default_factory=dict)
    # pins: list[int] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self._load_config_gpio(CONFIG_GPIO, "in")
        self._load_config_gpio(CONFIG_GPIO, "out")
        self._load_config_gpio(CONFIG_GPIO, "in_one_wire")


    def _load_config_gpio(self, config_file: str, dir: str):
        try:
            config_data = read_config_gpio(CONFIG_GPIO, dir)
        except Exception as e:
            print(f"Erro na leitura arquivo json. {e}")
            sys.exit()

        selected_keys = ["type", "name", "gpio"]
        for key, value in config_data.items():
            value["gpio"] = value["gpio1"] if self.type == "odd" else value["gpio2"]
            filter_dict = {key: value[key] for key in selected_keys}

            if dir == "in":
                self.inputs[key] = filter_dict
            elif dir == "out":
                self.outputs[key] = filter_dict
            else:
                self.onewire[key] = filter_dict   

    
    def turn_on_device(self, tag):
        print(f"Turn on: {tag}")
        PIN = self.outputs[tag].get("gpio")
        print(PIN)
        
        # GPIO.setup(PIN, GPIO.OUT)
        # GPIO.output(PIN, True)
    
    def turn_off_device(self, tag):
        print(f"Turn on: {tag}")
        PIN = self.outputs[tag].get("gpio")
        print(PIN)
        # GPIO.setup(PIN, GPIO.OUT)
        # GPIO.output(PIN, True)
        return self.re
        # command == "write":
        # print(command)
        # # GPIO.setup(PIN, GPIO.IN)
        
    def read_pin(self, tag):
        print(f"Turn on: {tag}")
        PIN = self.outputs[tag].get("gpio")
        print(PIN)
            
    
    def setup_mode_gpio(self, set_bcm: bool = True, set_warning: bool = False,):
        # GPIO.setwarnings(set_warning)
        # if set_bcm:
        #     GPIO.setmode(GPIO.BCM)
        # else:
        #     GPIO.setmode(GPIO.BOARD)
        pass
    
    def setup_devices_turn_off(self):
        
        for device in self.outputs.values():
            pin = (device.get("gpio"))
            print(pin, end=" ")
            # GPIO.setup(PIN, GPIO.OUT)
            # GPIO.output(PIN, False)
        print("\n")
        
    def setup_sensors(self):
        for sensor in self.inputs.values():
            pin = (sensor.get("gpio"))
            print(pin, end=" ")
            # GPIO.setup(PIN, GPIO.IN)
        print("\n")

    # def toggle_on_off_devices(self, command: str):
    #     for device in self.outputs:
    #         pin = (device.get("gpio"))
    #         print(pin, end=" ")
            
    #         if command == "read":
    #             print(command)
    #             # GPIO.setup(PIN, GPIO.IN)
            
    #         elif command == "write":
    #             print(command)
    #             # GPIO.setup(PIN, GPIO.IN)
           
    #         else:
    #             print("Comando não encontrado")
        
    #     print("\n")


def main():
    bd = BoardDistributed()
    print("^--" * 28)
    print("Board Distributed")
    print("^--" * 28)
    print(f"board: {bd.board}")
    print(f"room: {bd.room}")
    print(f"ip: {bd.ip}")
    print(f"ip_server: {bd.ip_server}")
    print(f"port_server: {bd.port_server}")
    print(f"type: {bd.type}")

    print("---" * 28)
    print(bd.inputs)
    print("---" * 28)
    print(bd.outputs)
    print("---" * 28)
    print(bd.onewire)
    print("---" * 28)
    bd.setup_devices_turn_off()
    bd.setup_sensors()
    print("---" * 28)
# def main():
    # print(
    #     textwrap.dedent(
    #         """\
    #          A   B   C
    #        ------------
    #     1 ┆  {0} │ {1} │ {2}
    #       ┆ ───┼───┼───
    #     2 ┆  {3} │ {4} │ {5}
    #       ┆ ───┼───┼───
    #     3 ┆  {6} │ {7} │ {8}
    # """
    #     ).format("a", "b", "c", "d", "e", "f", "g", "h", "i")
    # )

    # x = BoardCentral()
    # print("=^-^" * 50)
    # print("Board Central")
    # print(x.create_json("arquivo.json"))
    # print(x)
    # print("=^-^" * 50)
    # print(f"board: {x.board}")
    # print(f"room: {x.room}")
    # print(f"ip: {x.ip}")
    # print(f"ip_server: {x.ip_server}")
    # print(f"port_server: {x.port_server}")
    # print(f"type: {x.type}")
    
    # y = BoardDistributed()
    # print("=^-^" * 50)
    # print("Board Distributed")
    # print("=^-^" * 50)
    # print(f"board: {y.board}")
    # print(f"room: {y.room}")
    # print(f"ip: {y.ip}")
    # print(f"ip_server: {y.ip_server}")
    # print(f"port_server: {y.port_server}")
    # print(f"type: {y.type}")
    # print("= =" * 60)
    # print("Outputs:")
    # print("-" * 10)
    # print(y.outputs)
    # print("= =" * 60)
    # print("Imputs:")
    # print("-" * 10)
    # print(y.inputs)
    # print("= =" * 60)


if __name__ == "__main__":
    main()


# Estudar essa divisão (encapsulação)
# ==============================================================================================================================

# class PaymentStatus(Enum):
#     CANCELLED = "cancelled"
#     PENDING = "pending"
#     PAID = "paid"


# class PaymentStatusError(Exception):
#     pass


# @dataclass
# class deviceItem:
#     name: str
#     price: int
#     quantity: int

#     @property
#     def total_price(self) -> int:
#         return self.price * self.quantity


# @dataclass
# class Order:
#     items: list[deviceItem] = field(default_factory=list)
#     _payment_status: PaymentStatus = PaymentStatus.PENDING

#     def add_item(self, item: deviceItem):
#         self.items.append(item)

#     def set_payment_status(self, status: PaymentStatus) -> None:
#         if self._payment_status == PaymentStatus.PAID:
#             raise PaymentStatusError(
#                 "You can't change the status of an already paid order."
#             )
#         self._payment_status = status

#     @property
#     def total_price(self) -> int:
#         return sum(item.total_price for item in self.items)
# ==============================================================================================================================
# @dataclass
# class device_handler:

#     board: str = field(init=False)
#     room: str = field(init=False)
#     ip: str = field(init=False)
#     ip_server: str = field(init=False)
#     port_server: str = field(init=False)
#     type: str = field(init=False)
#     outputs: list[dict[str, str]] = field(default_factory=list)
#     inputs: list[dict[str, str]] = field(default_factory=list)

#     def __post_init__(self):
#         self.board = socket.gethostname()
#         self.ip = socket.gethostbyname(self.board)
#         self._load_config_board(CONFIG_BOARD)
#         self._load_output_gpio(CONFIG_GPIO)
#         self._load_input_gpio(CONFIG_GPIO)

#     def _load_config_board(self, config_file: str):
#         config_data = read_config(config_file, self.board)
#         self.board = config_data.get("board")
#         self.room = config_data.get("room")
#         self.ip_server = config_data.get("ip_server")
#         self.port_server = config_data.get("port_server")
#         self.type = config_data.get("type")

#     def _load_output_gpio(self, config_file: str):
#         config_data = read_config(config_file, "outputs")

#         for device in config_data:
#             clean = "gpio1" if self.type == "odd" else ["gpio2"]
#             [device.pop(key) for key in clean]
#             # device.dict(exclude={clean})

#             self.outputs.append(device)

#     def _load_input_gpio(self, config_file: str):
#         config_data = read_config(config_file, "inputs")

#         for device in config_data:
#             clean = "gpio1" if self.type == "odd" else ["gpio2"]
#             [device.pop(key) for key in clean]

#             self.inputs.append(device)
