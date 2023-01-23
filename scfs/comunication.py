import struct
from time import sleep

from serial import Serial


class ModbusUart:
    def __init__(self):
        self.crc16_table = self.create_crc16_table()
        self.serial_com = self.config_port()

    def config_port(self, baudrate=9600):
        while True:
            try:
                serial_port = Serial("/dev/ttyS0", baudrate)

            except Exception as e:
                print("Failed to open uart serial port")
                sleep(1)

            else:
                print("Uart serial port opened")
                return serial_port

    def read_data(self, bytes):
        return self.serial_com.read(bytes)

    def write_data(self, data):
        self.serial_com.write(data)

    def create_crc16_table(self):
        crc16_table = []

        for byte in range(256):
            crc = 0x0000
            for _ in range(8):
                if (byte ^ crc) & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
                byte >>= 1

            crc16_table.append(crc)
        return crc16_table

    def calc_crc16(self, data, crc_table):
        crc = 0x0000

        for a in data:
            crc = crc_table[(crc ^ a) & 0xFF] ^ (crc >> 8)

        byte1 = crc >> 8
        byte2 = crc & 0xFF

        return [byte2, byte1]

    def crc16(self, data):
        crc = 0xFFFF
        for i in range(len(data)):
            crc = crc ^ data[i]
            for _ in range(8):
                if (crc & 0x0001) == 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1

        byte1 = crc >> 8
        byte2 = crc & 0xFF
        return [byte2, byte1]

    def validade_crc(self, message):
        end_data = len(message) - 2
        data = message[:end_data]
        rec_crc = message[end_data:]

        calc_crc = self.calc_crc16(data, self.crc16_table)

        print(calc_crc, rec_crc)
        return rec_crc == calc_crc


if __name__ == "__main__":

    # slave_id = 0x01  # endereço ESP32
    # code_func = 0x23  # função solicita
    # sub_code = 0xC3  # solicita temperatura interna
    # mat_1 = 0x01  # primeiro digito da matricula
    # mat_2 = 0x02  # segundo digito da matricula
    # mat_3 = 0x02  # tercero digito da matricula
    # mat_4 = 0x01  # quarto digito da matricula

    # message = [slave_id, code_func, sub_code, mat_1, mat_2, mat_3, mat_4]

    # crc_table = create_crc16_table()
    # crc = calc_crc16(message, crc_table)

    # print(message)
    # print(bytes(message))
    # message += crc
    # print(crc)
    # print(message)
    # print("==================================")
    # valid_crc = validade_crc(message, crc_table)

    # if valid_crc:
    #     print("crc is valid")

    # print("==================================")
    # INTERNAL_TEMPERATURE = b"\x01\x23\xC1\x05\x06\x08\x02\x4c\x8e"
    # INTERNAL = b"\x01\x23\xC1\x05\x06\x08\x02"

    # msg_test = [0, 35, 195, 0, 0, 0, 0, 67, 66]
    # valid_crc = validade_crc(msg_test, crc_table)

    # print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    # if valid_crc:
    #     print("crc is valid")
    # else:
    #     print("crc is invalid")
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++")
