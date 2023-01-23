from time import sleep

import RPi.GPIO as GPIO

RESISTOR = 23
COOLER = 24


class PWMController:
    def __init__(self, resistor=RESISTOR, cooler=COOLER):
        self.resistor = resistor
        self.cooler = cooler
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.resistor, GPIO.IN)
        if GPIO.input(resistor):
            print("resistor estava ativado")

        GPIO.setup(self.cooler, GPIO.IN)
        if GPIO.input(cooler):
            print("coller estava ativado")

        GPIO.setup(self.resistor, GPIO.OUT)
        GPIO.setup(self.cooler, GPIO.OUT)
        self.pwm1 = GPIO.PWM(self.resistor, 100)
        self.pwm2 = GPIO.PWM(self.cooler, 100)

    def set_duty_cycle(self, duty_cycle):
        if duty_cycle >= 0:
            print(f"set_duty_cycle > 0 {duty_cycle}")
            self.pwm2.start(0)
            self.pwm1.start(duty_cycle)
        else:
            print(f"set_duty_cycle < 0 {duty_cycle}")
            self.pwm1.start(0)
            self.pwm2.start(-duty_cycle)

    def update_duty_cycle(self, duty_cycle):
        if duty_cycle >= 0:
            print(f"update_duty_cycle > 0 {duty_cycle}")
            self.pwm1.ChangeDutyCycle(duty_cycle)
        else:
            print(f"update_duty_cycle < 0 {duty_cycle}")
            self.pwm2.ChangeDutyCycle(duty_cycle)

    def stop(self):
        print("Parando tudo!!")
        self.pwm1.stop()
        self.pwm2.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    pwm = PWMController()

    pwm.set_duty_cycle(100)
    sleep(100)

    pwm.set_duty_cycle(-100)
    sleep(20)

    pwm.stop()
