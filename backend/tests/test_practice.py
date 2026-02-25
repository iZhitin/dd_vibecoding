from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_current_user
from app.core.database import get_db
from app.main import app
from app.models.card import Card
from app.models.practice_session import PracticeSession, SessionStatus
from app.models.user import User


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
def mock_db():
    from unittest.mock import AsyncMock, MagicMock

    class MockResult:
        def __init__(self, data):
            self._data = data

        def scalars(self):
            class MockItems:
                def __init__(self, d):
                    self._d = d

                def all(self):
                    return self._d

                def first(self):
                    return self._d[0] if self._d else None
            return MockItems(self._data)

    async def mock_execute(stmt):
        stmt_str = str(stmt).lower()
        if "practice_sessions" in stmt_str and "status = " in stmt_str:
            return MockResult([])
        if "cards" in stmt_str:
            cards = [
                Card(
                    id=UUID(f"00000000-0000-0000-0000-0000000000{i:02d}"),
                    user_id=UUID("00000000-0000-0000-0000-000000000001"),
                    word=f"word_{i}",
                    context_sentence="context",
                    weight=1.0,
                )
                for i in range(12)
            ]
            return MockResult(cards)
        if "practice_logs" in stmt_str:
            class MockLog:
                user_sentence = "Test sentence"
            return MockResult([MockLog()])
        return MockResult([])

    async def mock_refresh(instance):
        from datetime import UTC, datetime
        if not getattr(instance, "id", None):
            instance.id = UUID("00000000-0000-0000-0000-000000000004")
        if not getattr(instance, "created_at", None):
            instance.created_at = datetime.now(UTC)

    db = AsyncMock()
    db.add = MagicMock()
    db.refresh = AsyncMock(side_effect=mock_refresh)
    db.execute = AsyncMock(side_effect=mock_execute)
    return db


@pytest.fixture
def mock_db_with_active_session():
    from unittest.mock import AsyncMock, MagicMock

    class MockResult:
        def __init__(self, data):
            self._data = data

        def scalars(self):
            class MockItems:
                def __init__(self, d):
                    self._d = d

                def all(self):
                    return self._d

                def first(self):
                    return self._d[0] if self._d else None
            return MockItems(self._data)

    async def mock_execute(stmt):
        stmt_str = str(stmt).lower()
        if "practice_sessions" in stmt_str:
            return MockResult(
                [
                    PracticeSession(
                        id=UUID("00000000-0000-0000-0000-000000000999"),
                        status=SessionStatus.ACTIVE,
                    )
                ]
            )
        if "cards" in stmt_str:
            return MockResult([])
        return MockResult([])

    db = AsyncMock()
    db.add = MagicMock()
    db.execute = AsyncMock(side_effect=mock_execute)
    return db


@pytest.fixture
async def client(mock_db, current_user):
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
async def client_with_active_session(mock_db_with_active_session, current_user):
    app.dependency_overrides[get_db] = lambda: mock_db_with_active_session
    app.dependency_overrides[get_current_user] = lambda: current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_daily_practice_returns_10_cards(client: AsyncClient, mock_db):
    response = await client.get("/api/practice/daily")
    assert response.status_code == 200

    data = response.json()
    assert "session_id" in data
    assert len(data["cards"]) == 10

    for card_data in data["cards"]:
        assert "word" in card_data
        assert "translation" not in card_data
        assert card_data["previous_sentence"] == "Test sentence"


@pytest.mark.asyncio
async def test_get_daily_practice_existing_active_session(client_with_active_session: AsyncClient):
    response = await client_with_active_session.get("/api/practice/daily")
    assert response.status_code == 200

    data = response.json()
    assert data["session_id"] == "00000000-0000-0000-0000-000000000999"
    assert len(data["cards"]) == 0
