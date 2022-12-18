import asyncio
import logging

import websockets.client

logger = logging.getLogger(__name__)


# ================================================================================
async def send_sensor_reading(websocket):
    mock_temp = "Temp: 75º c"
    while True:
        await websocket.send(mock_temp)


# #########################################################################################################
async def receiver(message):
    print(message)


# ================================================================================
async def sender():
    message = "Mensagem padrão do Cliente!"
    return message


# ================================================================================
async def sender_handler(websocket):
    n = 0
    while True:
        message = await sender()
        await websocket.send(f"{n}: {message}")
        n = n + 1
        await asyncio.sleep(1.0)


# ================================================================================
async def receiver_handler(websocket):
    async for message in websocket:
        await receiver(message)


# ================================================================================
async def handler(websocket):
    receiver_task = asyncio.create_task(receiver_handler(websocket))
    sender_task = asyncio.create_task(sender_handler(websocket))
    done, pending = await asyncio.wait([receiver_task, sender_task], return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()


# ================================================================================
async def connector(host: str, port: int):
    uri = f"ws://{host}:{port}"
    print(f"uri: {uri}")

    async with websockets.client.connect(uri) as websocket:
        await handler(websocket)


# #########################################################################################################

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    asyncio.run(connector(host="localhost", port=4000))
