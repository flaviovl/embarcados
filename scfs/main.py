import signal
from time import sleep

from rich.prompt import Confirm, Prompt
from run import curve_mode, dash_mode, terminal_mode
from src.comm import ModbusUart
from src.controller import OvenController
from src.pid import PIDController
from src.pwm import PWMController
from utils import msg_down, msg_init

prompt = Prompt()


def signal_handler(sig, frame):
    oven.set_control_mode("dashboard")
    oven.set_operation(False)
    oven.set_system_power(False)
    oven.comm.close_serial_port()
    pwm.stop()
    msg_down()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    mbu = ModbusUart()
    pid = PIDController()
    pwm = PWMController()
    oven = OvenController(mbu)
    msg_init()

    while True:
        control_mode = prompt.ask(
            "[bold black]> Modo de controle? [blue][C][/]urva [blue][D][/]ashboard [blue][T][/]erminal",
            choices=["c", "d", "t"],
        )

        if control_mode == "t":
            sleep(1)
            oven.set_control_mode("terminal")
            terminal_mode(oven, pid, pwm)

        elif control_mode == "d":
            sleep(1)
            oven.set_control_mode("dashboard")
            dash_mode(oven, pid, pwm)

        else:
            sleep(1)
            oven.set_control_mode("curve")
            curve_mode(oven, pid, pwm)
