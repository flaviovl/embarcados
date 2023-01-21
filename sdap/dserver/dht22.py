import time

import adafruit_dht
import board

# (GPIO 18) - (Board 12)
dhtDevice = adafruit_dht.DHT22(board.D18)


while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

# ------------------------------------------------------------------------------------------------------------

import datetime
import time

import adafruit_dht
import board

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)

e = datetime.datetime.now()
date = "%s-%s-%s" % (e.day, e.month, e.year)
t = time.localtime()
current_time = time.strftime("%H%M%S", t)
file = open("humidityValues" + date + "_" + current_time + ".txt", "w")
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        t = time.local
        current_time = time.strftime("%H:%M:%S", t)
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        str = (
            "time="
            + current_time
            + "   temp={0:0.1f}ºC   humidity={1:0.1f}%".format(temperature_c, humidity)
        )
        print(str)
        file.write(str + "\n")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        # raise error

    time.sleep(2.0)
