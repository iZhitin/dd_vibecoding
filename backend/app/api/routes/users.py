from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import TimezoneUpdate, UserRead

router = APIRouter(prefix="/api/me", tags=["users"])


@router.get("", response_model=UserRead)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> UserRead:
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        timezone=current_user.timezone,
        streak_current=current_user.streak_current,
        streak_frozen_count=current_user.streak_frozen_count,
        last_practice_at=current_user.last_practice_at,
    )


@router.post("/timezone", response_model=UserRead)
async def update_timezone(
    data: TimezoneUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRead:
    current_user.timezone = data.timezone
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return UserRead(
        id=current_user.id,
        email=current_user.email,
        timezone=current_user.timezone,
        streak_current=current_user.streak_current,
        streak_frozen_count=current_user.streak_frozen_count,
        last_practice_at=current_user.last_practice_at,
    )
