import os
from datetime import datetime
from typing import List

import httpx
from database.db_connection import CConnection
from dotenv import load_dotenv
from sqlalchemy import update
from sqlalchemy.future import select

from .models import Bet
from .schemas import BetCreate

load_dotenv()


class BetService:
    def __init__(self, connection: CConnection):
        """ Initialize the BetService with a db connection. """
        self.connection = connection

    async def create_bet(self, bet_data: BetCreate) -> Bet:
        """ Create a new bet """
        async with self.connection.get_session() as session:
            new_bet = Bet(
                event_id=bet_data.event_id,
                amount=bet_data.amount,
                status=1,
                timestamp=datetime.utcnow()
            )
            session.add(new_bet)
            await session.commit()
            await session.refresh(new_bet)
            return new_bet

    async def list_bets(self) -> List[Bet]:
        """ Retrieve a list of all bets """
        async with self.connection.get_session() as session:
            result = await session.execute(select(Bet))
            return result.scalars().all()

    async def update_bet_status(self, event_id: int, status: int):
        """ Update the status of bets associated with a given event """
        async with self.connection.get_session() as session:
            await session.execute(
                update(Bet)
                .where(Bet.event_id == event_id)
                .values(status=status)
            )
            await session.commit()


async def get_available_events():
    """ Fetch a list of available events from line_provider """
    async with httpx.AsyncClient() as client:
        response = await client.get(os.getenv("LINE_PROVIDER_URL"))
        response.raise_for_status()
        return response.json()
