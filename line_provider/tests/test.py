from datetime import datetime
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_connection import CConnection
from app.models import Event, Base
from main import app
from app.service import EventService
from pydantic import BaseModel, root_validator
from decimal import Decimal

db_connection = CConnection()
event_service = EventService(connection=db_connection)


class EventCreate(BaseModel):
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
async def test_client():
    """Create a test client for HTTP requests."""
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture(scope="function")
async def test_event(db_session: AsyncSession):
    """Create a test event in the database."""
    event_data = EventCreate(
        coefficient=1.5,
        deadline=datetime(2024, 12, 31, 23, 59, 59),
        status=1
    )
    event = await event_service.create_event(event_data)
    return event


@pytest.mark.asyncio
async def test_create_event(test_client: TestClient):
    """Test event creation by sending a POST request."""
    event_data = EventCreate(
        coefficient=2.0,
        deadline=datetime(2024, 12, 31, 23, 59, 59),
        status=1
    )
    response = test_client.post("/events/", json=event_data.dict())
    assert response.status_code == 201
    assert float(response.json()["coefficient"]) == event_data.coefficient
    assert response.json()["status"] == event_data.status


@pytest.mark.asyncio
async def test_get_event(test_client: TestClient, test_event: Event):
    """Test retrieving an event by its ID."""
    response = test_client.get(f"/events/{test_event.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_event.id
    assert float(response.json()["coefficient"]) == float(test_event.coefficient)


@pytest.mark.asyncio
async def test_update_event(test_client: TestClient, test_event: Event):
    """Test updating an event's coefficient and status."""
    update_data = EventCreate(
        coefficient=2.0,
        deadline=datetime(2024, 12, 31, 23, 59, 59),
        status=2
    )
    response = test_client.put(f"/events/{test_event.id}", json=update_data.dict(exclude_unset=True))
    assert response.status_code == 200
    assert float(response.json()["coefficient"]) == update_data.coefficient
    assert response.json()["status"] == update_data.status


@pytest.mark.asyncio
async def test_delete_event(test_client: TestClient, test_event: Event):
    """Test deleting an event by its ID."""
    response = test_client.delete(f"/events/{test_event.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_event.id


@pytest.mark.asyncio
async def test_list_events(test_client: TestClient):
    """Test retrieving a list of all events."""
    response = test_client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
