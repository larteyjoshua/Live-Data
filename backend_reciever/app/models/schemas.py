from typing import List, Optional, Text
from pydantic import BaseModel
from datetime import datetime


class Notification(BaseModel):
    time: datetime
    action: str
