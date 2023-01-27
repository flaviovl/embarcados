import struct
from time import sleep

from src.comm import ModbusUart
from src.config import (
    GET_INTERNAL_TEMPERATURE,
    GET_REFERENCE_TEMPERATURE,
    NO_REPLY,
    OFF,
    ON,
    READ_COMMAND,
    REPLY,
    SEND_CONTROL_MODE_CURVE,
    SEND_CONTROL_MODE_DASHBOARD,
    SEND_CONTROL_SIGNAL,
    SEND_EXTERNAL_TEMPERATURE,
    SEND_OPERATION_STATUS_OFF,
    SEND_OPERATION_STATUS_ON,
    SEND_REFERENCE_TEMPERATURE,
    SEND_SYSTEM_STATUS_OFF,
    SEND_SYSTEM_STATUS_ON,
)

from .bme280 import get_temp_bme280


class OvenController:
    def __init__(self, comm: ModbusUart) -> None:
        self.comm = comm
        self.system_status = None
        self.control_mode = None
        self.operation_status = None
        self.set_initial_config()

    def set_initial_config(self):
        self.set_system_power(OFF)
        self.set_operation(OFF)
        self.set_control_mode(OFF)

    def read_command(self):
        reply = self.send_message(READ_COMMAND)
        return struct.unpack("<I", reply[3:7])[0]

    def send_message(self, data, bytes_to_read=REPLY):
        self.comm.write_data(data)
        sleep(0.1)
        reply = self.comm.read_data(bytes_to_read)
        if reply:
            if self.comm.validade_crc(list(reply)):
                return reply
            else:
                print("reply invalid CRC")

    def send_control_signal(self, signal):
        """D1 - Envio do sinal de controle (Resistor / Ventoinha)"""

        message = SEND_CONTROL_SIGNAL
        message += struct.pack("<i", signal)
        crc = self.comm.calc_crc16(message)
        message += struct.pack("<H", crc)

        self.send_message(message, NO_REPLY)

    def send_reference_temperature(self, temperature):
        """D2 - envio da temperatura de referência modo debug ou curva de referência"""

        message = SEND_REFERENCE_TEMPERATURE
        message += struct.pack("<f", temperature)
        crc = self.comm.calc_crc16(message)
        message += struct.pack("<H", crc)

        self.send_message(message, NO_REPLY)

    def send_external_temperature(self, temperature):
        """D6 - envio da temperatura externa(ambiente)"""

        message = SEND_EXTERNAL_TEMPERATURE
        message += struct.pack("<f", temperature)
        crc = self.comm.calc_crc16(message)
        message += struct.pack("<H", crc)

        self.send_message(message, NO_REPLY)

    def read_external_temperature(self):
        return get_temp_bme280()

    def read_internal_temperature(self):
        reply = self.send_message(GET_INTERNAL_TEMPERATURE)
        return struct.unpack("<f", reply[3:7])[0]

    def read_reference_temperature(self):
        reply = self.send_message(GET_REFERENCE_TEMPERATURE)
        return struct.unpack("<f", reply[3:7])[0]

    def set_system_power(self, turn_on):
        if turn_on:
            reply = self.send_message(SEND_SYSTEM_STATUS_ON)
            self.system_status = 1
        else:
            reply = self.send_message(SEND_SYSTEM_STATUS_OFF)
            self.system_status = 0

        return reply

    def set_operation(self, turn_on):
        if turn_on:
            reply = self.send_message(SEND_OPERATION_STATUS_ON)
            self.operation_status = ON
        else:
            reply = self.send_message(SEND_OPERATION_STATUS_OFF)
            self.operation_status = OFF

        return reply

    def set_control_mode(self, mode):
        """D4 - determina qual a temperautra de referência que irá aparecer no dashboard"""

        if mode in {"curve", 1}:
            reply = self.send_message(SEND_CONTROL_MODE_CURVE)
            self.control_mode = ON

        elif mode in {"dashboard", "terminal", 0}:
            reply = self.send_message(SEND_CONTROL_MODE_DASHBOARD)
            self.control_mode = OFF

        return reply
