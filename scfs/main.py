import struct
from time import sleep

from bme280 import read_bme280
from config import (
    GET_INTERNAL_TEMPERATURE,
    GET_REFERENCE_TEMPERATURE,
    READ_COMMAND,
    SEND_CONTROL_MODE_CURVE,
    SEND_CONTROL_MODE_TERMINAL,
    SEND_CONTROL_SIGNAL,
    SEND_EXTERNAL_TEMPERATURE,
    SEND_OPERATION_STATUS_OFF,
    SEND_OPERATION_STATUS_ON,
    SEND_REFERENCE_TEMPERATURE,
    SEND_SYSTEM_STATUS_OFF,
    SEND_SYSTEM_STATUS_ON,
)

from trabalhos.scfs.comm import ModbusUart


class OvenController:
    def __init__(self, comm: ModbusUart) -> None:
        self.comm = comm
        self.set_initial_config()

    def set_initial_config(self):
        self.system_status = self.send_message(SEND_OPERATION_STATUS_OFF)
        self.control_mode = self.send_message(SEND_SYSTEM_STATUS_OFF)
        self.operation_status = self.send_message(SEND_CONTROL_MODE_TERMINAL)

    def read_command(self):
        response = self.send_message(READ_COMMAND)
        return struct.unpack("<I", response[3:7])[0]

    def send_message(self, data, bytes_to_read=9):
        self.comm.write_data(data)
        sleep(0.1)
        response = self.comm.read_data(bytes_to_read)

        if self.comm.validade_crc(list(response)):
            return response

    def send_control_signal(self, signal):
        """D1 - Envio do sinal de controle (Resistor / Ventoinha)"""

        message = SEND_CONTROL_SIGNAL
        message += struct.pack(">I", signal)
        crc = self.comm.calc_crc16(message)
        message += struct.pack(">H", crc)

        # Ver se tem retorno para validar
        self.send_message(message)

    def send_reference_temperature(self, temperature):
        """D2 - envio da temperatura de referência modo debug ou curva de referência"""

        message = SEND_REFERENCE_TEMPERATURE
        message += struct.pack(">f", temperature)
        crc = self.comm.calc_crc16(message)
        message += struct.pack(">H", crc)

        self.send_message(message)

    def read_external_temperature(self):
        return read_bme280()

    def read_internal_temperature(self):
        response = self.send_message(GET_INTERNAL_TEMPERATURE)
        return struct.unpack("<I", response[3:7])[0]

    def read_reference_temperature(self):
        response = self.send_message(GET_REFERENCE_TEMPERATURE)
        return struct.unpack("<I", response[3:7])[0]

    def set_system_power(self, turn_on: bool):
        if turn_on:
            response = self.send_message(SEND_SYSTEM_STATUS_ON)
            self.system_status = 1
        else:
            response = self.send_message(SEND_SYSTEM_STATUS_OFF)
            self.system_status = 0

        return response

    def set_operation(self, turn_on: bool):
        if turn_on:
            response = self.send_message(SEND_OPERATION_STATUS_ON)
            self.operation_status = 1
        else:
            response = self.send_message(SEND_OPERATION_STATUS_OFF)
            self.operation_status = 0

        return response

    def set_control_mode(self, mode: str):
        """D4 - determina qual a temperautra de referência que irá aparecer no dashboard"""

        if mode == "curve":
            response = self.send_message(SEND_CONTROL_MODE_CURVE)
            self.control_mode = 1

        elif mode == "dashboard":
            response = self.send_message(SEND_CONTROL_MODE_DASHBOARD)
            self.control_mode = 0

        return response
