def create_crc16_table():
    crc16_table = []

    for byte in range(256):
        crc = 0x0000
        for _ in range(8):
            if (byte ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
            byte >>= 1

        crc16_table.append(crc)

    return crc16_table


def calculate_crc16(data, crc_table):
    crc = 0x0000

    for a in data:
        crc = crc_table[(crc ^ a) & 0xFF] ^ (crc >> 8)

    byte1 = crc >> 8
    byte2 = crc & 0xFF

    return [byte2, byte1]


if __name__ == "__main__":

    slave_id = 0x01  # endereço ESP32
    code_func = 0x23  # função solicita
    sub_code = 0xC3  # solicita temperatura interna
    mat_1 = 0x01  # primeiro digito da matricula
    mat_2 = 0x02  # segundo digito da matricula
    mat_3 = 0x02  # tercero digito da matricula
    mat_4 = 0x01  # quarto digito da matricula

    message = [slave_id, code_func, sub_code, mat_1, mat_2, mat_3, mat_4]

    crc_table = create_crc16_table()
    crc = calculate_crc16(message, crc_table)

    print(message)
    print(bytes(message))
    message += crc
    print(crc)
    print(message)
    print(bytes(message))
