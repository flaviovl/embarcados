import signal
from time import sleep

import RPi.GPIO as GPIO
from rich import print

RESISTOR = 23
COOLER = 24


class PWMController:
    def __init__(self, resistor=RESISTOR, cooler=COOLER, frequency=100):
        self.resistor = resistor
        self.cooler = cooler
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.resistor, GPIO.OUT)
        GPIO.setup(self.cooler, GPIO.OUT)
        self.pwm_resistor = GPIO.PWM(self.resistor, frequency)
        self.pwm_cooler = GPIO.PWM(self.cooler, frequency)

    def start(self, duty_cycle=0):
        self.pwm_resistor.start(duty_cycle)
        self.pwm_cooler.start(duty_cycle)
        return "[red]Starting:[/] [green]PWM!"

    def update_duty_cycle(self, duty_cycle):
        if duty_cycle >= 0:
            msg = f"[red bold]♨ [#FAEBD7]Heating [#FA8072]{duty_cycle:>3}%[red bold] ⬆ [/]"  
            self.pwm_cooler.ChangeDutyCycle(0)
            self.pwm_resistor.ChangeDutyCycle(duty_cycle)
        else:
            msg = f"[#B0E0E6]❄ Cooling [#008B8B]{-duty_cycle:>3}%[/] ⬇ [/]"
            self.pwm_resistor.ChangeDutyCycle(0)

            if -duty_cycle < 40:
                self.pwm_cooler.ChangeDutyCycle(40)
            else:
                self.pwm_cooler.ChangeDutyCycle(-duty_cycle)
        return msg

    def stop(self):
        self.pwm_cooler.stop()
        self.pwm_resistor.stop()
        return "[red]Stopping:[/] [green]PWM!"

    def clear_gpio(self):
        GPIO.cleanup()
        return "[red]Cleaning:[/] [gree]GPIO!"
