import asyncio
import logging

import websockets.server

logger = logging.getLogger(__name__)

# ======================================================================================================
async def receiver(message):
    print(message)


# ======================================================================================================
async def sender():
    message = "Mensagem padrão do servidor!"
    return message


# ======================================================================================================
async def sender_handler(websocket):
    n = 0
    while True:
        message = await sender()
        await websocket.send(f"{n}: {message}")
        n = n + 1
        await asyncio.sleep(4.0)


# ======================================================================================================
async def receiver_handler(websocket):
    async for message in websocket:
        await receiver(message)


# ======================================================================================================
async def handler(websocket):
    receiver_task = asyncio.create_task(receiver_handler(websocket))
    sender_task = asyncio.create_task(sender_handler(websocket))
    done, pending = await asyncio.wait([receiver_task, sender_task], return_when=asyncio.FIRST_COMPLETED)

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
        await asyncio.Future()


# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

if __name__ == "__main__":
    asyncio.run(main())
