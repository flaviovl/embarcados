import csv
import json
import socket
import signal
import sys
from time import sleep
from rich import print

from rich.console import Console

console = Console(width=100)

def read_csv(filename):
    rows = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        rows.extend(iter(csvreader))
    return rows[1:]

def write_csv(row, filename):
    with open(filename, "a") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(row)

def get_board_config(config_file):
    board = socket.gethostname()
    
    try:
        config_data = read_config_board(config_file, board)

    except Exception as e:
        print(f"Error reading file json. {e}")
        sys.exit()
        
    return {
        "board": board,
        "oven": config_data["oven"],
        "ip": config_data["host"],
        "dashboard": config_data["dashboard"]
    }
    
def read_config_board(config_file, board):
    with open(config_file) as file:
        data = json.load(file)
        return data.get(board) 

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


def msg_init(board):
    console.clear()
    console.rule("[#4682B4]Trabalho II - FSE - Forno de Soldagem", style="bright_yellow")
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
    console.log(f"[#4682B4]{board['board']}: {board['ip']} - forno {board['oven']}")
    console.line()
    console.log("[blue]⏺[/] Configuring Raspberry Pi GPIO...")
    sleep(0.2)
    console.log("[blue]⏺[/] Configuring Raspberry Pi I2C...")
    sleep(0.2)
    console.log("[blue]⏺[/] Configuring UART serial communication...")
    sleep(0.2)
    console.log("[#006400]⏺ Ready setup...")
    sleep(0.5)
    console.line()
    link_dash = board['dashboard']
    console.log(f"[blue][link={link_dash}]link dashboad thingsboard[/link]")
    console.rule(style="grey58")
    console.line()
