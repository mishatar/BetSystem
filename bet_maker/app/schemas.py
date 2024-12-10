from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class BetCreate(BaseModel):
    event_id: int
    amount: Decimal


class BetResponse(BaseModel):
    id: int
    event_id: int
    amount: Decimal
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True
