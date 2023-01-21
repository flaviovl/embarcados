import asyncio
import logging
from email.message import Message

import websockets.exceptions
import websockets.server

logger = logging.getLogger(__name__)
connected = set()

# ======================================================================================================
async def receiver(message):
    # print("--" * 40)
    # print("14 - receiver()")
    # print("++" * 10, end="\n\n")
    print("==" * 25)
    print("Tratando com a msg recebida - asyncio.sleep(30)")
    print("==" * 25)
    await asyncio.sleep(30.0)
    print(f"Mensagem foi tratada: {message}")


# ======================================================================================================
async def sender():
    print("--" * 40)
    print("24 - sender()")
    print("++" * 10, end="\n\n")

    msg1 = "1ª parte - "
    print(msg1)
    print("asyncio.sleep(2)")
    await asyncio.sleep(2.0)

    msg2 = "2ª parte - "
    print(msg2)
    print("asyncio.sleep(2)")
    await asyncio.sleep(2.0)

    msg3 = "3ª parte - "
    print(msg3)
    print("asyncio.sleep(2)")
    await asyncio.sleep(2.0)

    message = msg1 + msg2 + msg3 + "Servidor"
    print("Mensagem montada: asyncio.sleep(2)")

    await asyncio.sleep(2.0)
    return message


# ======================================================================================================
async def sender_handler(websocket):
    print("--" * 40)
    print("53 - sender_handler()")
    print("++" * 10, end="\n\n")
    n = 0
    while True:
        print("linha 58 - await sender()")
        message = await sender()
        print("linha 60 - await ws.send()")
        await websocket.send(f"{n}: {message}")
        print(" ->" * 13)
        print((f"{n}: Mensagem enviada: {message}"))
        print(" ->" * 13)
        print(f"linha 63 - n = {n} - asyncio.sleep(40)")
        n = n + 1
        await asyncio.sleep(40.0)


# ======================================================================================================
async def receiver_handler(websocket):
    print("--" * 40)
    print("71 - receiver_handler()")
    print("++" * 10, end="\n\n")
    try:
        print("72 - Antes async for")
        async for message in websocket:  ## Fica aqui aguardando msg

            print("\n")
            print("<-  " * 13)
            print(f"79 - message: {message}")
            print("<-  " * 13)
            print("\n")

            print("83 - Antes do await receiver(message)")
            await receiver(message)  # para para decidir o que fazer com a msg
            # print("<-  " * 10)
            print("86 - Apos do await receiver(message)")
            print("==" * 25)

    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

    finally:
        connected.remove(websocket)


# ======================================================================================================
async def handler(websocket):
    print("98 - handler()")
    print(".." * 10, end="\n\n")
    print()
    connected.add(websocket)
    print(connected)
    print("--" * 40)

    receiver_task = asyncio.create_task(receiver_handler(websocket))
    print(f"receiver_task: {receiver_task}")
    sender_task = asyncio.create_task(sender_handler(websocket))
    print(f"sender_task  : {sender_task}")
    done, pending = await asyncio.wait([receiver_task, sender_task], return_when=asyncio.FIRST_COMPLETED)
    print(f"done: {done}")
    print(f"pending: {pending}")

    for task in pending:
        task.cancel()


# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
async def main():
    print("=-" * 40)
    print("[Starting server..........]")
    print("Aguardando Cliente.")
    print("=-" * 40)
    # async with websockets.serve(handler, "localhost", 8001):
    async with websockets.server.serve(handler, "localhost", 4000):
        print("*" * 10)
        await asyncio.Future()  # para nessa linha
        print("*" * 20)  # nao chega nessa linha vai para handler


# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

if __name__ == "__main__":
    asyncio.run(main())


# art = """\
#     ______ ____  _____             ____ ____  ___    ____
#    / ____/ ___// ____/           / ___// __ \/   |  / __ \
#   / /_   \__ \/ __/    ______    \__ \/ / / / /| | / /_/ /
#  / __/  ___/ / /___   /_____/   ___/ / /_/ / ___ |/ ____/
# /_/    /____/_____/            /____/_____/_/  |_/_/
#
# Sistema Distribuído de Automação Predial
# """
