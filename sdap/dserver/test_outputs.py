from time import sleep

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.OUT)  # Alarme
GPIO.setup(18, GPIO.OUT)  # Lampada 1
GPIO.setup(23, GPIO.OUT)  # Lampada 2
GPIO.setup(24, GPIO.OUT)  # Ar Cond
GPIO.setup(25, GPIO.OUT)  # Projetor

GPIO.output(8, True)  # liga Alarme
sleep(2)
GPIO.output(18, True)  # Liga Lampada 1
sleep(2)
GPIO.output(23, True)  # Liga Lampada 2
sleep(2)
GPIO.output(24, True)  # Liga Ar Cond
sleep(2)
GPIO.output(25, True)  # Liga Projetor

sleep(5)

# Desliga tudo

GPIO.output(8, False)
GPIO.output(18, False)
GPIO.output(23, False)
GPIO.output(24, False)
GPIO.output(25, False)

GPIO.cleanup
