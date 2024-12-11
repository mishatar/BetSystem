from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class BetCreate(BaseModel):
    event_id: int
    amount: Decimal


class BetResponse(BaseModel):
    id: int
    event_id: int
    amount: Decimal
    status: int
    timestamp: datetime

    class Config:
        orm_mode = True


class EventStatusUpdate(BaseModel):
    event_id: int
    status: int
