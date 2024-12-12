from app.schemas import EventCreate, EventResponse, EventUpdate
from database.db_connection import CConnection
from fastapi import APIRouter, HTTPException, status

from .service import EventService

router = APIRouter()

db_connection = CConnection()
event_service = EventService(connection=db_connection)


@router.post("/events/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate):
    try:
        return await event_service.create_event(event)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/events/", response_model=list[EventResponse], status_code=status.HTTP_200_OK)
async def list_events():
    return await event_service.get_events()


@router.get("/events/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def get_event(event_id: int):
    event = await event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.put("/events/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def update_event(event_id: int, event: EventUpdate):
    try:
        return await event_service.update_event(event_id, event)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/events/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def delete_event(event_id: int):
    try:
        return await event_service.delete_event(event_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
