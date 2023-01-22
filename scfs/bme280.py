from time import sleep

import bme280
from smbus2 import SMBus


def read_bme280(port, addr):
    with SMBus(port) as i2c_bus:
        calib_params = bme280.load_calibration_params(i2c_bus, addr)

        data = bme280.sample(i2c_bus, addr, calib_params)
        temperature = data.temperature
        pressure = data.pressure
        humidity = data.humidity

        print(f"Temperatura : {temperature}")
        print(f"Pressao     : {pressure}")
        print(f"humidade    : {humidity}")

    return temperature
