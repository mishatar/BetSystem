import pytest
from httpx import AsyncClient
from main import app
from app.schemas import BetCreate
from app.models import Bet, Event
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


@pytest.fixture(scope="module")
async def test_event(db_session: AsyncSession):
    event_data = {
        "coefficient": 1.5,
        "deadline": datetime(2024, 12, 31, 23, 59, 59),
        "status": 1
    }
    event = Event(
        coefficient=event_data["coefficient"],
        deadline=event_data["deadline"],
        status=event_data["status"]
    )

    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)

    yield event

    await db_session.delete(event)
    await db_session.commit()


@pytest.fixture(scope="module")
async def test_bet(db_session: AsyncSession, test_event: Event):
    bet_data = BetCreate(
        event_id=test_event.id,
        amount=100.00,
        status=1,
        timestamp=datetime.utcnow()
    )
    bet = Bet(
        event_id=bet_data.event_id,
        amount=bet_data.amount,
        status=bet_data.status,
        timestamp=bet_data.timestamp
    )

    db_session.add(bet)
    await db_session.commit()
    await db_session.refresh(bet)

    yield bet

    await db_session.delete(bet)
    await db_session.commit()


@pytest.mark.asyncio
async def test_create_bet(test_event: Event):
    bet_data = {
        "event_id": test_event.id,
        "amount": 150.00,
        "status": 1,
        "timestamp": datetime.utcnow().isoformat()
    }

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post("/bets/", json=bet_data)

    assert response.status_code == 201
    assert response.json()["amount"] == bet_data["amount"]
    assert response.json()["status"] == bet_data["status"]
    assert response.json()["event_id"] == bet_data["event_id"]


@pytest.mark.asyncio
async def test_get_bet(test_bet: Bet):
    bet_id = test_bet.id

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(f"/bets/{bet_id}")

    assert response.status_code == 200
    assert response.json()["id"] == bet_id


@pytest.mark.asyncio
async def test_update_bet(test_bet: Bet):
    bet_id = test_bet.id
    update_data = {"amount": 200.0, "status": 2}

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.put(f"/bets/{bet_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["amount"] == update_data["amount"]
    assert response.json()["status"] == update_data["status"]


@pytest.mark.asyncio
async def test_delete_bet(test_bet: Bet):
    bet_id = test_bet.id

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.delete(f"/bets/{bet_id}")

    assert response.status_code == 200
    assert response.json()["id"] == bet_id
