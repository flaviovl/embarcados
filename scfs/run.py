import datetime
from time import perf_counter, sleep

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.prompt import Prompt
from src.config import (
    CANCEL,
    CURVE,
    DASHBOARD,
    OFF,
    ON,
    START_OPER,
    STOP_OPER,
    TOGGLE_MODE,
    TURN_OFF_OVEN,
    TURN_ON_OVEN,
)
from utils import read_csv, write_csv

console = Console(width=100)
prompt = Prompt()


def run_command(command, oven, pid, pwm):

    if command == TURN_ON_OVEN:
        if oven.system_status:
            print("[yellow bold]⚠ [yellow]The system is already ON")
        else:
            oven.set_system_power(True)
            print("[green bold]↗ [green]System ON")

    elif command == TURN_OFF_OVEN:
        if oven.system_status:
            print("[red bold]↘ [red]System OFF")
            oven.set_control_mode(DASHBOARD)
            oven.set_operation(False)
            oven.set_system_power(False)
        else:
            print("[yellow bold]⚠ [yellow]The system is already OFF")

        return CANCEL

    elif command == START_OPER:
        if oven.system_status and not oven.operation_status:
            print("[green bold]↗ [green]Operation started")
            oven.set_operation(ON)
            oven.set_control_mode(oven.control_mode)
            pwm.start()
            return ON
        else:
            print(
                "[yellow bold]⚠ [/]It is [red]not possible to start[/] operation with the oven switched off"
            )

    elif command == STOP_OPER:
        if oven.operation_status:
            print("[red bold dark]↘ [red]Operation OFF")
            oven.set_operation(OFF)
            oven.set_control_mode(OFF)
            pwm.stop()
        else:
            print(
                "[yellow bold]⚠ [/]It is [red]not possible to stop working[/] when it is not working"
            )

        return CANCEL

    elif command == TOGGLE_MODE:
        if oven.operation_status:
            print("It is [yellow]not possible to change modes[/] with the oven in operation")

        elif oven.control_mode == CURVE:
            oven.set_control_mode(DASHBOARD)
            console.clear()
            dash_mode(oven, pid, pwm)
        else:
            oven.set_control_mode(CURVE)
            console.clear()
            curve_mode(oven, pid, pwm)


def curve_mode(oven, pid, pwm):
    oven.set_system_power(True)
    oven.set_operation(True)
    console.line()
    console.rule("Curve Mode")

    rows = iter(read_csv())
    _, init_temp = next(rows)

    console.line(),
    print(
        Panel(
            f"[#4682B4]Adjust to start temperature:[green{init_temp}°",
            style="#4F4F4F",
            border_style="#A9A9A9",
            width=100,
        )
    )
    console.line()

    oven.send_reference_temperature(float(init_temp))
    set_temperature(oven, pid, pwm, float(init_temp))

    console.line(2)
    console.rule(style="#4682B4")
    console.print("[red]〽[/] Start following a predefined temperature curve", style="grey58")
    console.rule(style="#4682B4")
    console.line(2)

    while True:
        period, temperature = next(rows)
        tr = float(temperature)

        print(f"[#4682B4]Predefined temperature: [grey58 bold][{tr:.0f}° in {period}s]")

        oven.send_reference_temperature(tr)
        set_time(oven, pid, pwm, period, tr)
        console.line(2)
        console.rule(style="black")


def dash_mode(oven, pid, pwm):
    console.line()
    console.rule("Dashboard Mode")
    print("[#4682B4]Starting control on the dashboard!!")
    console.line()

    while True:
        command = oven.read_command()
        run = run_command(command, oven, pid, pwm)

        tr = oven.read_reference_temperature()
        ti = oven.read_internal_temperature()
        te = oven.read_external_temperature()
        pid.update_reference_temperature(tr)

        if oven.operation_status:
            pid_sig = pid.pid_control(ti)
            oven.send_control_signal(pid_sig)
            msg = pwm.update_duty_cycle(pid_sig)
            print(f"[dark]{msg} [blue]{ti:.1f}°[/] / [green]{tr}°")

        sleep(0.5)


def terminal_mode(oven, pid, pwm):
    console.line()
    stay = True
    while stay:
        console.clear()
        console.rule("Debug Mode", style="red")
        console.line()
        print("[#4682B4]Starting control on the terminal!!")
        console.line()

        print("  🔶 [blue]1. [white]Ler temperatura externa:")
        print("  🔶 [blue]2. [white]Ler temperatura interna:")
        print("  🔶 [blue]3. [white]Ler temperatura de referencia:")
        print("  🔶 [blue]4. [white]Ler comandos (UART):")
        print("  🔶 [blue]5. [white]Alternar modo de controle(curva/dash):")
        print("  🔶 [blue]6. [white]Enviar temperatura de referencia:")
        print("  🔶 [blue]7. [white]Enviar temperatura externa:")
        print("  🔶 [blue]8. [white]Envia Sinal de controle (resistor/fan):")
        print("  🔶 [blue]9. [white]Sair:")
        console.line()

        option = prompt.ask(
            "[white bold]Opção:", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        )
        console.line()

        if option == "1":
            te = oven.read_external_temperature()
            print(f"[black]TE = [/][blue]{te}°")
            input()

        elif option == "2":
            ti = oven.read_internal_temperature()
            print(f"[black]TI = [/][blue]{ti}°")
            input()

        elif option == "3":
            tr = oven.read_reference_temperature()
            print(f"[black]TR = [/][blue]{tr}°")
            input()

        elif option == "4":
            period = Prompt.ask(
                "[white]Choose a time by reading commands", choices=["5", "10", "30", "60", "120"]
            )
            print("[black]Test the commands using the dashboard:")
            console.line()
            print("[blue]Commands:")

            n = int(period)
            while n:
                command = oven.read_command()
                run_command(command, oven, pid, pwm)
                sleep(1)
                n = n - 1

        elif option == "5":
            if oven.control_mode == CURVE:
                oven.set_control_mode(DASHBOARD)
            else:
                oven.set_control_mode(CURVE)
            print("[black]switched mode [green]successfully")
            input()

        elif option == "6":
            tr = Prompt.ask(
                "[white]Choose a reference temperature to send", choices=["15", "38", "60", "80"]
            )
            oven.send_reference_temperature(float(tr))
            print("[black]See the answer in the [green]dashboard")
            input()

        elif option == "7":
            te = Prompt.ask(
                " [[white]Choose a external temperature to send", choices=["25", "30", "50", "70"]
            )
            oven.send_external_temperature(float(te))
            print("[black]See the answer in the [green]dashboard")
            input()

        elif option == "8":
            signal = Prompt.ask(
                "[white]Choose a control signal (resistor/fan)",
                choices=["-100", "-50", "0", "50", "100"],
            )
            oven.send_control_signal(int(signal))
            print("[black]See the answer in the [green]dashboard")
            input()

        elif option == "9":
            print("[yellow]Closing DEBUG MODE......")
            oven.set_control_mode(OFF)
            oven.set_operation(OFF)
            oven.set_system_power(OFF)
            pwm.stop()
            stay = False
            sleep(2)
            console.clear()
            console.rule(f"Trabalho Forno FSE", style="bright_yellow")
            console.line()

        else:
            "[red]Invalid option!"
            console.line()
            input()


def set_temperature(oven, pid, pwm, tr, delay=0.5):

    with Progress() as progress:
        last_error = int(oven.read_internal_temperature() - tr)
        last_error = abs(last_error) - 1  # aceita um erro de +- 1°

        task1 = progress.add_task("[green]Processing...", total=abs(last_error))

        while not progress.finished:
            ti = oven.read_internal_temperature()
            te = oven.read_external_temperature()
            pid.update_reference_temperature(tr)
            pid_sig = pid.pid_control(ti)
            oven.send_control_signal(pid_sig)

            msg = pwm.update_duty_cycle(pid_sig)
            desc = f"[dark]{msg} [red]{ti:.1f}°[/]/[green]{tr}°"
            error = ti - tr
            adv = abs(last_error - error)
            progress.update(task1, advance=adv, description=desc)

            last_error = error
            sleep(delay)

            command = oven.read_command()
            run = run_command(command, oven, pid, pwm)
            if run == CANCEL:
                continue


def set_time(oven, pid, pwm, period, tr, delay=0.5):

    with Progress() as progress:
        total = int(period)
        start_time = perf_counter()
        last_time = start_time

        task1 = progress.add_task("[green]Processing...", total=total)

        while not progress.finished:
            command = oven.read_command()
            run_command(command, oven, pid, pwm)

            ti = oven.read_internal_temperature()
            te = oven.read_external_temperature()
            pid.update_reference_temperature(tr)
            pid_sig = pid.pid_control(ti)
            oven.send_control_signal(pid_sig)

            msg = pwm.update_duty_cycle(pid_sig)
            desc = f"[dark]{msg} [red]{ti:.1f}°[/]/[green]{tr}°\n\n[[red]CTRL-C[/]] to exit"

            sleep(delay)

            adv = perf_counter() - last_time
            last_time = perf_counter()

            progress.update(task1, advance=adv, description=desc)

            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            row_log = [now, ti, te, tr, pid_sig]
            write_csv(row_log)

        progress.update(task1, description="[green bold]✔ Done!")
