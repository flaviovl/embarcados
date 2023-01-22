from time import sleep

import RPi.GPIO as GPIO
from scfs.config import (
    READ_COMMAND,
    SEND_CONTROL_MODE_DASH,
    SEND_OPERATION_STATUS_OFF,
    SEND_SYSTEM_STATUS_OFF,
)
from serial import Serial

PORT_I2C = 1
ADDR_I2C = 0x76

RESISTOR = 23
COLLER = 24


def read_serial_data(n):
    return serial_port.read(n)


def write_serial_data(data):
    serial_port.write(data)


def config_gpip():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RESISTOR, GPIO.OUT)
    GPIO.setup(COLLER, GPIO.OUT)


def config_serial_port():
    while True:
        try:
            serial_port = Serial("/dev/ttyS0", 9600)

        except Exception as e:
            print("Failed to open uart serial port")
            sleep(2)

        else:
            print("Uart serial port opened")
            return serial_port


def init_states():

    write_serial_data(SEND_OPERATION_STATUS_OFF)
    sleep(0.1)
    response = read_serial_data(7)
    print(list(response))

    write_serial_data(SEND_SYSTEM_STATUS_OFF)
    sleep(0.1)
    response = read_serial_data(7)
    print(list(response))

    write_serial_data(SEND_CONTROL_MODE_DASH)
    sleep(0.1)
    response = read_serial_data(7)
    print(list(response))


if __name__ == "__main__":
    config_gpip()
    serial_port = config_serial_port()

    if serial_port.isOpen() == False:
        serial_port.open()

    init_states()

    while True:
        write_serial_data(READ_COMMAND)
        sleep(0.1)
        response = read_serial_data(7)
        print(list(response))
        sleep(5)
