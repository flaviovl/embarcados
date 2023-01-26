from enum import Enum

# Lista de Comandos :
# =============================================================================================================================================
# Protocolo de comunicação com crc calculado - Mensagens fixas
# =============================================================================================================================================

READ_COMMAND = b"\x01\x23\xC3\x05\x06\x08\x02\x35\x4e"
GET_INTERNAL_TEMPERATURE = b"\x01\x23\xC1\x05\x06\x08\x02\x4c\x8e"
GET_REFERENCE_TEMPERATURE = b"\x01\x23\xC2\x05\x06\x08\x02\x08\x8e"
SEND_SYSTEM_STATUS_ON = b"\x01\x16\xD3\x05\x06\x08\x02\x01\x28\x44"  # Ligar sistema
SEND_SYSTEM_STATUS_OFF = b"\x01\x16\xD3\x05\x06\x08\x02\x00\xe9\x84"  # Desligar sistema
SEND_CONTROL_MODE_CURVE = b"\x01\x16\xD4\x05\x06\x08\x02\x01\x29\xf3"  # Modo Curva = 1 (mostra no dashboard temperatura enviada pelo comando xD2)
SEND_CONTROL_MODE_DASHBOARD = b"\x01\x16\xD4\x05\x06\x08\x02\x00\xe8\x33"  # Modo Fixo = 0 (mostra no dashboard temperatura dos botoes)
SEND_OPERATION_STATUS_ON = b"\x01\x16\xD5\x05\x06\x08\x02\x01\x28\x22"  # Ligar o forno
SEND_OPERATION_STATUS_OFF = b"\x01\x16\xD5\x05\x06\x08\x02\x00\xe9\xe2"  # Desligar o forno

# =============================================================================================================================================
# Protocolo de comunicação - Mensagens variaveis (add dado + crc)
# =============================================================================================================================================

SEND_CONTROL_SIGNAL = b"\x01\x16\xD1\x05\x06\x08\x02"  # + int 4 bytes (Resistor / Ventoinha)
SEND_REFERENCE_TEMPERATURE = b"\x01\x16\xD2\x05\x06\x08\x02"  # + float 4 bytes (envio da temperatura de referência - usando modo curva)
SEND_EXTERNAL_TEMPERATURE = b"\x01\x16\xD6\x05\x06\x08\x02"  # + float 4 bytes (temperatura ambient)

# =============================================================================================================================================
# Contantes
# =============================================================================================================================================

TURN_ON_OVEN = 0xA1  # 161
TURN_OFF_OVEN = 0xA2  # 162
START_OPER = 0xA3  # 163
STOP_OPER = 0xA4  # 164
TOGGLE_MODE = 0xA5  # 165
REPLY = 9
NO_REPLY = 0
OFF = 0
ON = 1
CURVE = 1
TERMINAL = 1
DASHBOARD = 0
CANCEL = -1
