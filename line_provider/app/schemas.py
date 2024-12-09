import decimal
from datetime import datetime

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    coefficient: decimal.Decimal
    deadline: datetime
    status: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S.%f')
        }


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    coefficient: decimal.Decimal = Field(default=None, gt=0)
    deadline: datetime = None
    status: int = None


class EventResponse(EventBase):
    id: int

    class Config:
        from_attributes = True
