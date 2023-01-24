import csv
from dataclasses import dataclass
from time import perf_counter, sleep

import datetime
from main import OvenController
from pid import PIDController
from pwm import PWMController
from rich import print
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from rich.table import Table
from scfs.comm import ModbusUart


def init_config():
    console.clear()
    console.line()
    console.log("Inicializando GPIO...")
    sleep(1)
    console.log("Inicializando modulo I2C...")
    sleep(1)
    console.log("Configurando serial uart...")
    sleep(1)
    console.log("Reiniciando sistema...")
    sleep(1)


def debug_mode():
    stay = True
    while stay:
        print("")
        print("\t1. Ler temperatura ambiente:")
        print("\t2. Ler temperatura interna:")
        print("\t3. Ler temperatura de referencia:")
        print("\t3. Ler comandos:")
        print("\t4. Atualizar TR:")
        print("\t5. Atualizar PWM:")
        print("\t6. Calcular PID:")
        print("\t7. Envia Sinal de controle UART:")
        print("\t8. Sair:")
        print("")

        option = prompt.ask("\tOpção:", choices=["1", "2", "3", "4", "5", "6", "7", "8"])

        if option == "8":
            stay = False


# ===================================================================================
def control_mode_dash():
    while True:
        command = oven.read_command()
        exec_command(command)

        tr = oven.read_reference_temperature()
        ti = oven.read_internal_temperature()
        te = oven.read_external_temperature()

        oven.send_reference_temperature(tr)

        pid.update_reference_temperature(tr)
        control_signal = pid.pid_control(ti)

        oven.send_control_signal(control_signal)
        pwm.update_duty_cycle(control_signal)


# ===================================================================================
def control_mode_curve():

    rows = iter(read_csv())
    start_time = perf_counter()
    duration, temp = next(rows)

    while True:
        command = oven.read_command()
        exec_command(command)

        tr = temp
        ti = oven.read_internal_temperature()
        te = oven.read_external_temperature()

        oven.send_reference_temperature(tr)

        pid.update_reference_temperature(tr)
        control_signal = pid.pid_control(ti)

        oven.send_control_signal(control_signal)
        pwm.update_duty_cycle(control_signal)

        sleep(0.5)
        
        if (start_time - perf_counter) >= duration:
            duration, temp = next(rows)
            
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        row_log = [now, ti, te, tr, control_signal]
        write_csv(row=row_log)
        

# ===================================================================================
def exec_command(command):

    if command == 165:
        mode = "dashboard" if oven.control_mode else "curve"
        oven.set_control_mode(mode)

    elif command == 161:
        oven.set_system_power(True)

    elif command == 162:  # deligar sistema
        oven.set_control_mode("dashboard")
        oven.set_operation(False)
        oven.set_system_power(False)
        oven.comm.close_serial_port()  # i2c é fechao de forma automatica (bloco with)
        pwm.stop()

    elif command == 163:
        oven.set_operation(True)

    elif command == 164:
        oven.set_operation(False)

    else:
        print("invalid command")


# ===================================================================================

def read_csv(filename="curva_reflow.csv"):
    rows = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        rows.extend(iter(csvreader))
    return rows[1:]

def write_csv(filename="logs.csv", row):
    with open(filename, "a") as csvfile:
        csvfile.writerow(row) 


# ===================================================================================

if __name__ == "__main__":
    init_config()

    console = Console()
    prompt = Prompt()

    mbu = ModbusUart()
    pid = PIDController()
    pwm = PWMController()

    oven = OvenController(mbu)

    while True:
        print("")
        control_mode = prompt.ask("Qual modo de controle?", choices=["curve", "dash", "debug"])

        if control_mode == "debug":
            debug_mode()

        elif control_mode == "dash":
            control_mode_dash()

        else:
            control_mode_curve()

        # cpf = int(prompt.ask("[green]digite seu [bold]CPF[/]: [/]"))
        # resposta = prompt.ask(f"Você digitou [red]{cpf}[/], este número está correto?")
        # if resposta.lower() in ("s", "sim"):
        #     print("ótimo")
        #     continuar = False
        # elif resposta.lower() in ("n", "não"):
        #     print("reiniciando...")
        # else:
        #     print('Digite apenas [red]"s"[/] ou [red]"n"[/]')

        # with console.status("[green]Preenchendo formulário[/]") as status:
        #     consultar_cpf()

        # print("[green]Seu CPF está pronto para um financiamento![/]")

        # table = Table(title="Financiamentos Disponíveis")
        # table.add_column("Meses")
        # table.add_column("Valor")
        # table.add_column("Taxa de juros")

        # table.add_row("12x", "R$1750,00", "7.5%")
        # table.add_row("36", "R$560,00", "12.0%")
        # table.add_row("72x", "R$360,00", "15.5%")

        # print(table)

        # tipo_financiamento = prompt.ask(
        #     "Qual financiamento deseja contratar?", choices=["12x", "36x", "72x"]
        # )

        # nome = input("Digite seu nome para finalizar: ")

        # print(
        #     f"[on blue][black]Parabéns [white]{nome}[/], você escolheu o financiamento de [green]{tipo_financiamento}[/][/][/]"
        # )
