import csv
import signal
import sys
from time import sleep

from rich.console import Console

console = Console(width=100)


def read_csv(filename="curva_reflow.csv"):
    rows = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        rows.extend(iter(csvreader))
    return rows[1:]


def write_csv(row, filename="logs/logs.csv"):
    with open(filename, "a") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(row)


def msg_down():
    console.clear()
    console.rule("Encerrando o sistema", style="red")
    console.line(2)
    console.log("[red]Ctrl+C -> was pressed...")
    sleep(1)
    console.line()

    console.log("🟡 Interropendo funcionamento (resistor e ventoinha)...")
    sleep(0.3)
    console.log("🟡 Desligando forno.")
    sleep(0.3)
    console.log("🟡 Limpando portas GPIO...")
    sleep(0.3)
    console.log("🟡 Encerrando modulo I2C...")  # i2c é fechao de forma automatica (bloco with)
    sleep(0.3)
    console.log("🟡 Fechando porta serial UART...")
    sleep(0.3)
    console.line()
    console.log("🟢 [green]Programa encerrado com sucesso...")
    console.line(2)

    sys.exit(0)


def msg_init():
    console.clear()
    console.rule("Trabalho Forno FSE", style="bright_yellow")
    console.line()
    print(
        """\
     ___________ ___________________           _________________ ___________ _________
     \_   _____//   _____/_   _____/          /   _____/_   ___ \\_   _____//   _____/
     |  ___)  \_____  \ |    __)_    ______  \_____  \/    \  \/  |  ___)  \_____  \ 
     |  \__   /        \|        \  /_____/  /        \     \____ |  \__   /        \ 
    /___  /  /_______  /_______  /          /_______  /\______  //___  /  /_______  / 
        \/           \/        \/                   \/        \/     \/           \/ 
                                            
                                            Sistema de Controle Forno de Soldagem"""
    )

    console.line()
    console.rule(style="grey58")
    console.log("Inicializando GPIO...")
    sleep(0.2)
    console.log("Inicializando modulo I2C...")
    sleep(0.2)
    console.log("Configurando serial UART...")
    sleep(0.2)
    console.log("Pronto...")
    console.rule(style="grey58")
    console.line()
