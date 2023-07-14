import random
import time
from app.utils.logging import log
import json
from collections import deque
import datetime
from app.utils.notification_helper import send_webhook
from fastapi import BackgroundTasks

my_queue = deque()


def generate_sensor_data():
    humidity: float = round(random.uniform(0, 100), 2)
    temperature: float = round(random.uniform(-20, 50), 2)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    log.info(humidity)
    log.info(temperature)
    data = {'humidity': humidity,
            'temperature': temperature,
            'time': current_time}
    return data


def create_sensor_object():
    data = generate_sensor_data()
    log.info(f"New sensor data: {data}")
    my_queue.append(data)
    log.info(len(my_queue))
    current_datetime = datetime.datetime.now()
    notice = {'time': str(current_datetime),
              'action': 'New Data Created Successfully'}
    send_webhook(notice)
    log.info(data)


async def send_generator():
    queue_size = len(my_queue)
    if queue_size > 0:
        item = my_queue.popleft()
        log.info(item)
        log.info('item sent',)
        return json.dumps(item)
