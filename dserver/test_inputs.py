import RPi.GPIO as GPIO
import os
from time import sleep

GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD)

# GPIO.setwarnings(False) 

presence_sensor = 7
smoke_sensor = 1
windom_sensor = 12
door_sensor = 16
people_in_sensor = 20 
people_out_sensor = 21

pins = [
    presence_sensor,
    presence_sensor
    smoke_sensor,
    windom_sensor,
    door_sensor,
    people_in_sensor, 
    people_out_sensor,
]

GPIO.setup(presence_sensor, GPIO.IN)     # Sensor Presenca
GPIO.setup(smoke_sensor, GPIO.IN)        #  Sensor Fumaça
GPIO.setup(windom_sensor, GPIO.IN)       # Sensor de Janela
GPIO.setup(door_sensor, GPIO.IN)         # Sensor de Porta
GPIO.setup(people_in_sensor, GPIO.IN)    # Controle entrada pessoas
GPIO.setup(people_out_sensor, GPIO.IN)   # Controle saída pessoas


def get_presence_sensor():
    pass

def get_smoke_sensor():
    pass

def get_windom_sensor():
    pass

def get_door_sensor():
    pass

def get_people_in_sensor():
    pass

def get_people_out_sensor():
    pass
   
GPIO.add_event_detect(presence_sensor, GPIO.RISING)
GPIO.add_event_detect(smoke_sensor, GPIO.RISING)
GPIO.add_event_detect(windom_sensor, GPIO.RISING)
GPIO.add_event_detect(door_sensor, GPIO.RISING)
GPIO.add_event_detect(people_in_sensor, GPIO.RISING)
GPIO.add_event_detect(people_out_sensor, GPIO.RISING)

while True:
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-" * 60)
    print("Aguardado sensores!")
    print("-" * 60)
    sleep(3)
    
    if GPIO.event_detected(presence_sensor):
        print("> Sensor de Presença foi ativado!")
        sleep(2)
    
    elif GPIO.event_detected(smoke_sensor):
        print("> Sensor de Fumaça foi ativado!")
        sleep(2)
    
    elif GPIO.event_detected(windom_sensor):
        print("> Sensor de Janela está ativado!")
        sleep(2)
    
    elif GPIO.event_detected(door_sensor):
        print("> Sensor de porta está ativado!")
        sleep(2)
    
    elif GPIO.event_detected(people_in_sensor):
        print("> Sensor de Entrada de Pessoa foi ativado!")
        sleep(2)
    
    elif GPIO.event_detected(people_out_sensor):
        print("> Sensor de Entrada de Pessoa foi ativado!")
        sleep(2)
    
    else:
        print("Nenhum evento detectado!")
        sleep(5)
        print("")
        print("x_x " * 5)
    
    print("\n\n")
    print("=*" * 20)
    print("\n\n")
    