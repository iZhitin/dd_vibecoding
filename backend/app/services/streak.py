from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def update_streak(user: User, db: AsyncSession) -> User:
    """
    Update user's streak based on their last practice time.
    Calculations are done in the user's timezone.
    """
    now_utc = datetime.now(UTC)
    timezone_str = user.timezone if user.timezone else "UTC"
    tz = ZoneInfo(timezone_str)

    today = now_utc.astimezone(tz).date()

    if user.last_practice_at is None:
        user.streak_current = 1
    else:
        # Ensure last_practice_at has tzinfo, assume UTC if missing
        last_prac = user.last_practice_at
        if last_prac.tzinfo is None:
            last_prac = last_prac.replace(tzinfo=UTC)
            
        last_practice_date = last_prac.astimezone(tz).date()
        delta_days = (today - last_practice_date).days

        if delta_days == 0:
            # Already practiced today, don't change streak
            pass
        elif delta_days == 1:
            # Practiced yesterday
            user.streak_current += 1
        elif delta_days == 2 and user.is_frozen and user.streak_frozen_count > 0:
            # Missed exactly one day, but user is frozen
            user.streak_frozen_count -= 1
            user.is_frozen = False
            user.streak_current += 1
        else:
            # Missed more than 1 day or missed 1 day without frozen status
            user.streak_current = 1

    user.last_practice_at = now_utc.replace(tzinfo=None)
    db.add(user)
    # The commit is typically handled by the caller, e.g., in `submit_practice`.
    # But the instruction says "Сохранить в БД." We can do `await db.flush()`
    # if we don't want to commit mid-transaction, or let caller commit.
    # The requirement asks to save, so we'll do flush so it's ready.
    await db.flush()

    return user
