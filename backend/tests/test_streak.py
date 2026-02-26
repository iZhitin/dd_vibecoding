import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest

from app.models.user import User
from app.services.streak import update_streak


@pytest.fixture
def mock_db():
    from unittest.mock import MagicMock
    db = AsyncMock()
    db.add = MagicMock()
    return db


@pytest.mark.asyncio
async def test_first_practice(mock_db):
    user = User(
        id=uuid.uuid4(),
        timezone="UTC",
        streak_current=0,
        streak_frozen_count=0,
        is_frozen=False,
        last_practice_at=None,
    )
    
    updated_user = await update_streak(user, mock_db)
    assert updated_user.streak_current == 1
    assert updated_user.last_practice_at is not None
    mock_db.add.assert_called_once_with(updated_user)
    mock_db.flush.assert_called_once()


@pytest.mark.asyncio
async def test_consecutive_days(mock_db):
    now = datetime(2026, 2, 26, 12, 0, tzinfo=UTC)
    yesterday = now - timedelta(days=1)
    
    user = User(
        id=uuid.uuid4(),
        timezone="UTC",
        streak_current=1,
        streak_frozen_count=0,
        is_frozen=False,
        last_practice_at=yesterday.replace(tzinfo=None),
    )
    
    with patch("app.services.streak.datetime") as mock_dt:
        mock_dt.now.return_value = now
        updated_user = await update_streak(user, mock_db)
        assert updated_user.streak_current == 2


@pytest.mark.asyncio
async def test_skip_day_resets(mock_db):
    now = datetime(2026, 2, 26, 12, 0, tzinfo=UTC)
    two_days_ago = now - timedelta(days=2)
    
    user = User(
        id=uuid.uuid4(),
        timezone="UTC",
        streak_current=5,
        streak_frozen_count=0,
        is_frozen=False,
        last_practice_at=two_days_ago.replace(tzinfo=None),
    )
    
    with patch("app.services.streak.datetime") as mock_dt:
        mock_dt.now.return_value = now
        updated_user = await update_streak(user, mock_db)
        assert updated_user.streak_current == 1


@pytest.mark.asyncio
async def test_same_day_no_change(mock_db):
    now = datetime(2026, 2, 26, 12, 0, tzinfo=UTC)
    earlier_today = now - timedelta(hours=2)
    
    user = User(
        id=uuid.uuid4(),
        timezone="UTC",
        streak_current=5,
        streak_frozen_count=0,
        is_frozen=False,
        last_practice_at=earlier_today.replace(tzinfo=None),
    )
    
    with patch("app.services.streak.datetime") as mock_dt:
        mock_dt.now.return_value = now
        updated_user = await update_streak(user, mock_db)
        assert updated_user.streak_current == 5


@pytest.mark.asyncio
async def test_freeze_preserves_streak(mock_db):
    now = datetime(2026, 2, 26, 12, 0, tzinfo=UTC)
    two_days_ago = now - timedelta(days=2)
    
    user = User(
        id=uuid.uuid4(),
        timezone="UTC",
        streak_current=5,
        streak_frozen_count=1,
        is_frozen=True,
        last_practice_at=two_days_ago.replace(tzinfo=None),
    )
    
    with patch("app.services.streak.datetime") as mock_dt:
        mock_dt.now.return_value = now
        updated_user = await update_streak(user, mock_db)
        # Missed 1 day but frozen, so streak continues to 6
        assert updated_user.streak_current == 6
        assert updated_user.is_frozen is False


@pytest.mark.asyncio
async def test_freeze_count_decreases(mock_db):
    now = datetime(2026, 2, 26, 12, 0, tzinfo=UTC)
    two_days_ago = now - timedelta(days=2)
    
    user = User(
        id=uuid.uuid4(),
        timezone="UTC",
        streak_current=5,
        streak_frozen_count=3,
        is_frozen=True,
        last_practice_at=two_days_ago.replace(tzinfo=None),
    )
    
    with patch("app.services.streak.datetime") as mock_dt:
        mock_dt.now.return_value = now
        updated_user = await update_streak(user, mock_db)
        
        assert updated_user.streak_current == 6
        assert updated_user.is_frozen is False
        assert updated_user.streak_frozen_count == 2
