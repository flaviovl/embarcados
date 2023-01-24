import signal
from time import sleep

import RPi.GPIO as GPIO

RESISTOR = 23
COOLER = 24


class PWMController:
    def __init__(self, resistor=RESISTOR, cooler=COOLER):
        self.resistor = resistor
        self.cooler = cooler
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.resistor, GPIO.OUT)
        GPIO.setup(self.cooler, GPIO.OUT)
        self.start_pwm()

    def start_pwm(self, frequency = 100):
        self.pwm_resistor = GPIO.PWM(self.resistor, frequency)
        self.pwm_cooler = GPIO.PWM(self.cooler, frequency)
        self.pwm_resistor.start(0)
        self.pwm_cooler.start(0)

    def update_duty_cycle(self, duty_cycle):
        if duty_cycle >= 0:
            print(f"Esquentando.... > 0: {duty_cycle}")
            self.pwm_cooler.ChangeDutyCycle(0)
            self.pwm_resistor.ChangeDutyCycle(duty_cycle)
        else:
            print(f"Esfriando..... < 0 {-duty_cycle}")
            self.pwm_resistor.ChangeDutyCycle(0)
            
            if -duty_cycle < 40:           
                self.pwm_cooler.ChangeDutyCycle(40)
            else:
                self.pwm_cooler.ChangeDutyCycle(-duty_cycle))

    def stop(self):
        print("Parando tudo!!")
        self.pwm_cooler.stop()
        self.pwm_resistor.stop()
        GPIO.cleanup()

