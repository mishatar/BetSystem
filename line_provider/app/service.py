from typing import List, Optional

from sqlalchemy.future import select

from app.models import Event
from app.schemas import EventCreate, EventUpdate
from database.db_connection import CConnection


class EventService:

    def __init__(self, connection: CConnection):
        """
        Initialize the EventService with a db connection.
        """
        self.connection = connection

    async def get_event(self, event_id: int) -> Optional[Event]:
        """
        Fetche a single event by id.
        """
        async with self.connection.get_session() as session:
            query = select(Event).where(Event.id == event_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_events(self) -> List[Event]:
        """
        Fetche all events from the database.
        """
        async with self.connection.get_session() as session:
            query = select(Event)
            result = await session.execute(query)
            return result.scalars().all()

    async def create_event(self, event_data: EventCreate) -> Event:
        """
        Create a new event in the database.
        """
        async with self.connection.get_session() as session:
            new_event = Event(**event_data.dict())
            session.add(new_event)
            await session.commit()
            return new_event

    async def update_event(self, event_id: int, event_data: EventUpdate) -> Event:
        """
        Update an existing event.
        """
        async with self.connection.get_session() as session:
            query = select(Event).where(Event.id == event_id)
            result = await session.execute(query)
            event = result.scalar_one_or_none()

            if not event:
                raise ValueError("Event not found")

            for key, value in event_data.dict(exclude_unset=True).items():
                setattr(event, key, value)

            await session.commit()
            await session.refresh(event)
            return event

    async def delete_event(self, event_id: int) -> Event:
        """
        Delete event from the database by id.
        """
        async with self.connection.get_session() as session:
            event = await self.get_event(event_id)
            if not event:
                raise ValueError(f"Event not found")
            await session.delete(event)
            await session.commit()
            return event
