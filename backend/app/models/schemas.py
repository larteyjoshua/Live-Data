from pydantic import BaseModel
from datetime import datetime


class SendData(BaseModel):
    humidity: float
    temperature: float


class Notification(BaseModel):
    time: datetime
    action: str
