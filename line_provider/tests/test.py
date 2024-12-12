from datetime import datetime

import pytest
from app.models import Event
from app.schemas import EventCreate
from httpx import AsyncClient
from main import app
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="module")
async def test_event(db_session: AsyncSession):
    event_data = EventCreate(
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

    yield event

    await db_session.delete(event)
    await db_session.commit()


@pytest.mark.asyncio
async def test_create_event():
    event_data = {
        "coefficient": 1.5,
        "deadline": "2024-12-31 23:59:59",
        "status": 1
    }

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post("/events/", json=event_data)

    assert response.status_code == 201
    assert response.json()["coefficient"] == event_data["coefficient"]
    assert response.json()["status"] == event_data["status"]


@pytest.mark.asyncio
async def test_get_event(test_event: Event):
    event_id = test_event.id

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(f"/events/{event_id}")

    assert response.status_code == 200
    assert response.json()["id"] == event_id


@pytest.mark.asyncio
async def test_update_event(test_event: Event):
    event_id = test_event.id
    update_data = {"coefficient": 2.0, "status": 2}

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.put(f"/events/{event_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["coefficient"] == update_data["coefficient"]
    assert response.json()["status"] == update_data["status"]


@pytest.mark.asyncio
async def test_delete_event(test_event: Event):
    event_id = test_event.id

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.delete(f"/events/{event_id}")

    assert response.status_code == 200
    assert response.json()["id"] == event_id
