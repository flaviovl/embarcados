from enum import Enum

# Lista de Comandos :
# =============================================================================================================================================
# MENSAGENS completas com crc
# =============================================================================================================================================

GET_INTERNAL_TEMPERATURE = b"\x01\x23\xC1\x05\x06\x08\x02\x4c\x8e"
# [1, 35, 193, 5, 6, 8, 2, 76, 142]
GET_REFERENCE_TEMPERATURE = b"\x01\x23\xC2\x05\x06\x08\x02\x08\x8e"
# [1, 35, 194, 5, 6, 8, 2, 8, 142]
READ_COMMAND = b"\x01\x23\xC3\x05\x06\x08\x02\x35\x4e"
# [1, 35, 195, 5, 6, 8, 2, 53, 78]
SEND_SYSTEM_STATUS_ON = b"\x01\x16\xD3\x05\x06\x08\x02\x01\x28\x44"  # Ligar sistema
# [1, 22, 211, 5, 6, 8, 2, 1, 40, 68]
SEND_SYSTEM_STATUS_OFF = b"\x01\x16\xD3\x05\x06\x08\x02\x00\xe9\x84"  # Desligar sistema
# [1, 22, 211, 5, 6, 8, 2, 0, 233, 132]
SEND_CONTROL_MODE_CURVE = b"\x01\x16\xD4\x05\x06\x08\x02\x01\x29\xf3"  # Modo Curva = 1 (mostra no dashboard temperatura enviada pelo comando xD2)
# [1, 22, 212, 5, 6, 8, 2, 1, 41, 243]
SEND_CONTROL_MODE_TERMINAL = b"\x01\x16\xD4\x05\x06\x08\x02\x00\xe8\x33"  # Modo Fixo = 0 (mostra no dashboard temperatura dos botoes)
# [1, 22, 212, 5, 6, 8, 2, 0, 232, 51]
SEND_OPERATION_STATUS_ON = b"\x01\x16\xD5\x05\x06\x08\x02\x01\x28\x22"  # Ligar o forno
# [1, 22, 213, 5, 6, 8, 2, 1, 40, 34]
SEND_OPERATION_STATUS_OFF = b"\x01\x16\xD5\x05\x06\x08\x02\x00\xe9\xe2"  # Desligar o forno
# [1, 22, 213, 5, 6, 8, 2, 0, 233, 226]

# =============================================================================================================================================
# MENSAGENS sem valor e crc
# =============================================================================================================================================

SEND_CONTROL_SIGNAL = b"\x01\x16\xD1\x05\x06\x08\x02"  # + int 4 bytes (Resistor / Ventoinha)
SEND_REFERENCE_SIGNAL = b"\x01\x16\xD2\x05\x06\x08\x02"  # + float 4 bytes (envio da temperatura de referência - usando modo curva)
SEND_ROOM_TEMPERATURE = b"\x01\x16\xD6\x05\x06\x08\x02"  # + float 4 bytes (temperatura ambient)

# =============================================================================================================================================
# Comandos  (READ_COMMAND - C3)


class COMMAND(Enum):
    TURN_ON_OVEN = 0xA1  # 161
    TURN_OFF_OVEN = 0xA2  # 162
    START_HEATING = 0xA3  # 163
    CANCEL = 0xA4  # 164
    MENU = 0xA5  # 165


# Menu : alterna entre o modo de Temperatura de Referência e Curva de Temperatura
