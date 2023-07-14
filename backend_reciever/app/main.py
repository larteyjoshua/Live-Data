from threading import Thread
from fastapi import FastAPI, Request, WebSocket, BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from app.utils.logging import log
import json
from queue import Queue
import http
from collections import deque
import asyncio
from sseclient import SSEClient
import requests
import asyncio
import aiohttp


message_queue = deque()


app = FastAPI(title='Hook and Socket')


@app.on_event("startup")
async def startup_event():
    url = 'http://localhost:8000/v1/events'
    await subscribeToEventSource(url)
    # asyncio.run(await subscribeToEventSource(url))


def send_message(message):
    message_queue.append(message)
    log.info(len(message_queue))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/new-notification",  status_code=http.HTTPStatus.ACCEPTED)
async def webhook(request: Request, backgroundTask: BackgroundTasks):
    payload = await request.body()
    data = json.loads(payload)
    backgroundTask.add_task(send_message, data)
    log.info(data)
    return {'message': 'Webhook received'}


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    ws_tx_thread = Thread(target=websocket_tx_task_wrapper,
                          args=(websocket, message_queue,))
    ws_tx_thread.start()

    while True:
        data = await websocket.receive_text()
        log.info(f"WS RX: {data}")


async def websocket_tx_task(ws, _q):
    log.info("Starting WS tx...")

    while True:
        if (len(_q) > 0):
            item = _q.popleft()
            await ws.send_text(item)


def websocket_tx_task_wrapper(ws, _q):
    asyncio.run(websocket_tx_task(ws, _q))


async def subscribeToEventSource(url: str):
    client = SSEClient(url)
    for event in client:
        log.info(event)
    response = requests.get(url, stream=True)  # Enable streaming response

    for line in response.json():
        if line:
            # Process the received event data
            log.info("Received event:", line)

    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url,) as resp:
    #         while True:
    #             event = await resp.text()
    #             if event == b'':
    #                 break
    #             print(event.decode())
    #             log.info(event.decode())
