from datetime import datetime
from sqlalchemy.future import select

from app.models import Bet
from app.schemas import BetCreate
from database.db_connection import CConnection


class BetService:
    def __init__(self, connection: CConnection):
        """ Initialize the EventService with a db connection. """
        self.connection = connection

    async def create_bet(self, bet_data: BetCreate):
        async with self.connection.get_session() as session:
            new_bet = Bet(
                event_id=bet_data.event_id,
                amount=bet_data.amount,
                status='',
                timestamp=datetime.utcnow()
            )
            session.add(new_bet)
            await session.commit()
            await session.refresh(new_bet)
            return new_bet

    async def list_bets(self):
        async with self.connection.get_session() as session:
            result = await session.execute(select(Bet))
            return result.scalars().all()
