import os
from datetime import datetime
from typing import List, Optional

import httpx
from app.models import Event
from app.schemas import EventCreate, EventUpdate
from database.db_connection import CConnection
from dotenv import load_dotenv
from sqlalchemy.future import select

load_dotenv()


class EventService:

    def __init__(self, connection: CConnection):
        """ Initialize the EventService with a db connection. """
        self.connection = connection

    async def get_event(self, event_id: int) -> Optional[Event]:
        """ Fetche a single event by id. """
        async with self.connection.get_session() as session:
            query = select(Event).where(Event.id == event_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_events(self) -> List[Event]:
        """ Fetche all events from the database. """
        async with self.connection.get_session() as session:
            query = select(Event).where(Event.deadline > datetime.utcnow())
            result = await session.execute(query)
            return result.scalars().all()

    async def create_event(self, event_data: EventCreate) -> Event:
        """ Create a new event in the database. """
        async with self.connection.get_session() as session:
            new_event = Event(**event_data.dict())
            session.add(new_event)
            await session.commit()
            return new_event

    async def update_event(self, event_id: int, event_data: EventUpdate) -> Event:
        """ Update an existing event. """
        async with self.connection.get_session() as session:
            query = select(Event).where(Event.id == event_id)
            result = await session.execute(query)
            event = result.scalar_one_or_none()

            if not event:
                raise ValueError("Event not found")

            data = event_data.dict(exclude_unset=True)
            for key, value in data.items():
                setattr(event, key, value)

            await session.commit()
            await session.refresh(event)
            await notify_bet_maker(event_id, data.get("status"))
            return event

    async def delete_event(self, event_id: int) -> Event:
        """ Delete event from the database by id. """
        async with self.connection.get_session() as session:
            event = await self.get_event(event_id)
            if not event:
                raise ValueError(f"Event not found")
            await session.delete(event)
            await session.commit()
            return event


async def notify_bet_maker(event_id, status):
    data = {
        "event_id": event_id,
        "status": status
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(os.getenv("BET_MAKER_CALLBACK_URL"), json=data)
            response.raise_for_status()
    except httpx.RequestError as e:
        print(f"Failed to notify bet-maker: {e}")
