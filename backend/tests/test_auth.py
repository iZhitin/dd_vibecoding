import datetime
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.security import create_magic_token
from app.main import app
from app.models.user import User


@pytest.fixture
def mock_db():
    db = AsyncMock()
    return db

@pytest.fixture
async def client(mock_db):
    from app.core.database import get_db
    app.dependency_overrides[get_db] = lambda: mock_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_login_creates_magic_link(client: AsyncClient, mock_db):
    class MockResult:
        def scalar_one_or_none(self): return None
    mock_db.execute.return_value = MockResult()
    mock_db.commit = AsyncMock()
    
    response = await client.post("/api/auth/login", json={"email": "newuser@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Magic link sent"}
    assert mock_db.add.called
    assert mock_db.commit.called

@pytest.mark.asyncio
async def test_verify_magic_link(client: AsyncClient, mock_db):
    class MockResult:
        def scalar_one_or_none(self): 
            return User(id=UUID("00000000-0000-0000-0000-000000000001"), email="test2@example.com")
    mock_db.execute.return_value = MockResult()

    token = create_magic_token("test2@example.com")
    
    response = await client.post("/api/auth/verify", json={"token": token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_verify_expired_magic_link(client: AsyncClient):
    with patch("app.core.security.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=20)  # noqa: E501
        mock_datetime.timedelta = datetime.timedelta
        token = create_magic_token("test_expired@example.com")

    response = await client.post("/api/auth/verify", json={"token": token})
    assert response.status_code == 401
