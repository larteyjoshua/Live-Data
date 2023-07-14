import requests
from app.utils.logging import log
import json
import time


def send_webhook(body):
    log.info(body)
    data = json.dumps(body)
    response = requests.post(
        "http://localhost:8800/new-notification", json=data)
    if response.status_code == 200:
        log.info("Webhook sent successfully")
    else:
        log.info("Failed to send webhook")
