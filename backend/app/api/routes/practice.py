import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.practice import (
    DailyPracticeResponse,
    PracticeSessionReviewResponse,
    PracticeSubmitRequest,
)
from app.services.practice import (
    generate_daily_session,
    get_practice_session_review,
    submit_practice,
)

router = APIRouter(prefix="/api/practice", tags=["practice"])


@router.get("/daily", response_model=DailyPracticeResponse)
async def get_daily_practice(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    session, practice_cards = await generate_daily_session(current_user.id, db)
    return DailyPracticeResponse(session_id=session.id, cards=practice_cards)


@router.post("/submit")
async def process_practice_submission(
    data: PracticeSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await submit_practice(current_user.id, data, db)
    return {"status": "ok"}


@router.get("/sessions/{session_id}/review", response_model=PracticeSessionReviewResponse)
async def get_session_review(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_practice_session_review(current_user.id, session_id, db)
