from time import sleep

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# CONSTANTS:
PRESENCE_SENSOR = 7
SMOKE_SENSOR = 1
WINDOW_SENSOR = 12
DOOR_SENSOR = 16
PEOPLE_ENTRY_SENSOR = 20
PEOPLE_EXIT_SENSOR = 21
ALARM = 8
LAMP1 = 18
LAMP2 = 23
AC = 24
PROJECTOR = 25


pins = [
    PRESENCE_SENSOR,
    SMOKE_SENSOR,
    WINDOW_SENSOR,
    DOOR_SENSOR,
    PEOPLE_ENTRY_SENSOR,
    PEOPLE_EXIT_SENSOR,
    ALARM,
    LAMP1,
    LAMP2,
    AC,
    PROJECTOR,
]


def get_status_devices():

    GPIO.setup(PRESENCE_SENSOR, GPIO.IN)
    GPIO.setup(SMOKE_SENSOR, GPIO.IN)
    GPIO.setup(WINDOW_SENSOR, GPIO.IN)
    GPIO.setup(DOOR_SENSOR, GPIO.IN)
    GPIO.setup(PEOPLE_ENTRY_SENSOR, GPIO.IN)
    GPIO.setup(PEOPLE_EXIT_SENSOR, GPIO.IN)
    GPIO.setup(ALARM, GPIO.IN)
    GPIO.setup(LAMP1, GPIO.IN)
    GPIO.setup(LAMP2, GPIO.IN)
    GPIO.setup(AC, GPIO.IN)
    GPIO.setup(PROJECTOR, GPIO.IN)

    print("=" * 60)
    print("Status dispositivos:")
    print("=" * 60)
    while True:
        alarm = GPIO.input(ALARM)
        lamp1 = GPIO.input(LAMP1)
        lamp2 = GPIO.input(LAMP2)
        ac = GPIO.input(AC)
        proj = GPIO.input(PROJECTOR)
        presence = GPIO.input(PRESENCE_SENSOR)
        smoke = GPIO.input(SMOKE_SENSOR)
        window = GPIO.input(WINDOW_SENSOR)
        door = GPIO.input(DOOR_SENSOR)
        entry = GPIO.input(PEOPLE_ENTRY_SENSOR)
        exit = GPIO.input(PEOPLE_EXIT_SENSOR)

        print(f" Status Alarme    : {alarm}")
        print(f" Status Lampada1  : {lamp1}")
        print(f" Status Lampada2  : {lamp2}")
        print(f" Status Ar_cond   : {ac}")
        print(f" Status Projetor  : {proj}")
        print(f" Sensor Preseça   : {proj}")
        print(f" Sendor de Fumaça : {proj}")
        print(f" Sensor de Janela : {proj}")
        print(f" Sensor de Porta  : {proj}")
        print(f" Entrada Pessoas  : {proj}")
        print(f" Saida de Pessoas : {proj}")

        print("")
        print("-" * 60, end="\n")
        sleep(2)


if __name__ == "__main__":
    get_status_devices()
    GPIO.cleanup


# def get_status_devices():
#     get_lamp1
#     get_alarm_system
#     get_lamp2
#     get_projector
#     get_air_conditioner
#     get_siren
