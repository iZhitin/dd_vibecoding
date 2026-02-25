import datetime
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_current_user
from app.core.security import create_access_token, create_magic_token
from app.main import app
from app.models.user import User


@pytest.fixture
def mock_db():
    from unittest.mock import AsyncMock, MagicMock
    db = AsyncMock()
    db.add = MagicMock()
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

@pytest.mark.asyncio
async def test_get_current_user_valid(mock_db):
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user = User(id=user_id, email="test@example.com")
    
    class MockResult:
        def scalar_one_or_none(self):
            return user
            
    mock_db.execute.return_value = MockResult()
    
    token = create_access_token(user_id)
    resolved_user = await get_current_user(token=token, db=mock_db)
    
    assert resolved_user.id == user_id
    assert resolved_user.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_current_user_missing_token(mock_db):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=None, db=mock_db)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_db):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="invalid_token", db=mock_db)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"

@pytest.mark.asyncio
async def test_get_current_user_not_found(mock_db):
    class MockResult:
        def scalar_one_or_none(self):
            return None
            
    mock_db.execute.return_value = MockResult()
    
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    token = create_access_token(user_id)
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token, db=mock_db)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "User not found"
