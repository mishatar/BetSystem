from database.db_connection import CConnection
from fastapi import APIRouter, HTTPException, status

from .schemas import BetCreate, BetResponse, EventStatusUpdate
from .service import BetService, get_available_events

router = APIRouter()

db_connection = CConnection()
bet_service = BetService(connection=db_connection)


@router.post("/bet", response_model=BetResponse, status_code=status.HTTP_201_CREATED)
async def place_bet(bet: BetCreate):
    try:
        return await bet_service.create_bet(bet)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bets", response_model=list[BetResponse], status_code=status.HTTP_200_OK)
async def get_bets():
    return await bet_service.list_bets()


@router.post("/events/status_update/", status_code=status.HTTP_200_OK)
async def event_status_update(status_update: EventStatusUpdate):
    try:
        await bet_service.update_bet_status(status_update.event_id, status_update.status)
        return {"message": "Status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/events", status_code=status.HTTP_200_OK)
async def get_events():
    try:
        return await get_available_events()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
