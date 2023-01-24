import struct
from time import sleep

from serial import Serial


class ModbusUart:
    def __init__(self):
        self.crc16_table = self.create_crc16_table()
        self.serial_com = self.config_port()
        self.open_serial_port()
        
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
    
    def open_serial_port(self)
        if self.serial_com.isOpen() == False:
            self.serial_com.open()

    def close_serial_port(self):
        self.serial_com.close()
    
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

    def calc_crc16(self, data):
        crc = 0x0000

        for a in data:
            crc = self.crc16_table[(crc ^ a) & 0xFF] ^ (crc >> 8)

        return crc
    
    
    def crc16(self, data):
        crc = 0xFFFF
        for i in range(len(data)):
            crc = crc ^ data[i]
            for _ in range(8):
                if (crc & 0x0001) == 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc


    def validade_crc(self, message):
        end_data = len(message) - 2
        data = message[:end_data]
        rec_crc = message[end_data:]

        calc_crc = self.calc_crc16(data)

        byte1 = calc_crc >> 8
        byte2 = calc_crc & 0xFF

        calc_crc = [byte2, byte1]
    
        print(rec_crc, calc_crc)
        return rec_crc == calc_crc
