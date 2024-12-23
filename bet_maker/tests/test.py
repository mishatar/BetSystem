from datetime import datetime
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Event, Bet, Base
from database.db_connection import CConnection
from main import app
from pydantic import BaseModel, root_validator
from decimal import Decimal

db_connection = CConnection()

class EventBase(BaseModel):
    coefficient: float
    deadline: datetime
    status: int

    @root_validator(pre=True)
    def convert_decimal_to_float(cls, values):
        """Convert coefficient from Decimal to float if needed."""
        if 'coefficient' in values and isinstance(values['coefficient'], Decimal):
            values['coefficient'] = float(values['coefficient'])
        return values

    def dict(self, *args, **kwargs):
        """Convert datetime to ISO 8601 string format."""
        data = super().dict(*args, **kwargs)
        if 'deadline' in data:
            data['deadline'] = data['deadline'].isoformat()
        return data


class BetBase(BaseModel):
    event_id: int
    amount: float
    timestamp: datetime
    status: int

    @root_validator(pre=True)
    def convert_decimal_to_float(cls, values):
        """Convert amount from Decimal to float if needed."""
        if 'amount' in values and isinstance(values['amount'], Decimal):
            values['amount'] = float(values['amount'])
        return values

    def dict(self, *args, **kwargs):
        """Convert timestamp to ISO 8601 string format."""
        data = super().dict(*args, **kwargs)
        if 'timestamp' in data:
            data['timestamp'] = data['timestamp'].isoformat()
        return data


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Provide a new database session for each test."""
    connection = CConnection()
    async with connection.get_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clear_db(db_session: AsyncSession):
    """Clear all tables in the database before each test."""
    for table in reversed(Base.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()

@pytest_asyncio.fixture(scope="module")
def test_client():
    """Create a test client for HTTP requests."""
    client = TestClient(app)
    return client


@pytest_asyncio.fixture(scope="function")
async def test_event(db_session):
    """Fixture to create a test event."""
    event_data = EventBase(
        coefficient=1.5,
        deadline=datetime(2024, 12, 31, 23, 59, 59),
        status=1
    )
    event = Event(
        coefficient=event_data.coefficient,
        deadline=event_data.deadline,
        status=event_data.status
    )
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)
    return event


@pytest_asyncio.fixture(scope="function")
async def test_bet(db_session, test_event):
    """Fixture to create a test bet."""
    bet_data = BetBase(
        event_id=test_event.id,
        amount=100.0,
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
    return bet


@pytest.mark.asyncio
async def test_create_bet(test_client: TestClient, test_event: Event):
    """Test creating a bet."""
    bet_data = {
        "event_id": test_event.id,
        "amount": 150.0,
        "timestamp": datetime.utcnow().isoformat()
    }
    response = test_client.post("/bet", json=bet_data)  # No await needed here
    assert response.status_code == 201
    assert response.json()["amount"] == str(bet_data["amount"])
    assert response.json()["event_id"] == bet_data["event_id"]
    assert response.json()["status"] == 1


@pytest.mark.asyncio
async def test_get_bets(test_client: TestClient, test_bet: Bet):
    """Test retrieving a list of bets."""
    response = test_client.get("/bets")  # No await needed here
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Ensure at least one bet is returned


@pytest.mark.asyncio
async def test_event_status_update(test_client: TestClient, test_event: Event):
    """Test updating an event's status."""
    status_update = {"event_id": test_event.id, "status": 2}
    response = test_client.post("/events/status_update/", json=status_update)  # No await needed here
    assert response.status_code == 200
    assert response.json()["message"] == "Status updated successfully"


@pytest.mark.asyncio
async def test_get_events(test_client: TestClient):
    """Test retrieving a list of available events."""
    response = test_client.get("/events")
    assert response.status_code == 400
    assert len(response.json()) >= 0

