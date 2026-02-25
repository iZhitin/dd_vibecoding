from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_current_user
from app.core.database import get_db
from app.main import app
from app.models.user import User


@pytest.fixture
def mock_db():
    from unittest.mock import AsyncMock, MagicMock

    db = AsyncMock()
    db.add = MagicMock()
    return db


@pytest.fixture
def current_user():
    return User(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        email="test@example.com",
        timezone="Europe/Moscow",
        streak_current=5,
        streak_frozen_count=1,
        last_practice_at=None,
    )


@pytest.fixture
async def client(mock_db, current_user):
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
async def unauth_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, current_user: User):
    response = await client.get("/api/me")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(current_user.id)
    assert data["email"] == current_user.email
    assert data["timezone"] == current_user.timezone
    assert data["streak_current"] == current_user.streak_current
    assert data["streak_frozen_count"] == current_user.streak_frozen_count


@pytest.mark.asyncio
async def test_get_me_unauth(unauth_client: AsyncClient):
    response = await unauth_client.get("/api/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_timezone(client: AsyncClient, mock_db, current_user: User):
    response = await client.post("/api/me/timezone", json={"timezone": "Europe/Berlin"})

    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "Europe/Berlin"

    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called


@pytest.mark.asyncio
async def test_update_timezone_invalid(client: AsyncClient):
    response = await client.post("/api/me/timezone", json={"timezone": "Invalid/Timezone"})

    assert response.status_code == 422
    data = response.json()
    assert "Invalid timezone: Invalid/Timezone" in data["detail"][0]["msg"]
