from fastapi import APIRouter, HTTPException, status
from app.schemas import BetCreate, BetResponse
from app.service import BetService

router = APIRouter()
bet_service = BetService()


@router.post("/bet", response_model=BetResponse, status_code=status.HTTP_201_CREATED)
async def place_bet(bet: BetCreate):
    try:
        return await bet_service.create_bet(bet)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bets", response_model=list[BetResponse], status_code=status.HTTP_200_OK)
async def get_bets():
    return await bet_service.list_bets()
