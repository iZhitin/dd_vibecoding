import uuid
from datetime import UTC, datetime

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.practice_log import PracticeLog
from app.models.practice_session import PracticeSession, SessionStatus
from app.schemas.practice import PracticeCardRead
from app.services.srs import select_practice_cards


async def generate_daily_session(
    user_id: uuid.UUID, db: AsyncSession
) -> tuple[PracticeSession, list[PracticeCardRead]]:
    """
    1. Check if there's an active session
    2. If not, create one
    3. Select 10 practice cards
    4. Find the last PracticeLog for each card to get the previous sentence
    """
    stmt = select(PracticeSession).where(
        PracticeSession.user_id == user_id,
        PracticeSession.status == SessionStatus.ACTIVE,
    )
    result = await db.execute(stmt)
    active_session = result.scalars().first()

    if active_session:
        session = active_session
    else:
        session = PracticeSession(
            user_id=user_id, status=SessionStatus.ACTIVE, started_at=datetime.now(UTC)
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)

    cards = await select_practice_cards(user_id, db, count=10)

    practice_cards: list[PracticeCardRead] = []
    for card in cards:
        log_stmt = (
            select(PracticeLog)
            .where(PracticeLog.card_id == card.id)
            .order_by(desc(PracticeLog.created_at))
            .limit(1)
        )
        log_res = await db.execute(log_stmt)
        last_log = log_res.scalars().first()

        practice_cards.append(
            PracticeCardRead(
                card_id=card.id,
                word=card.word,
                context_sentence=card.context_sentence,
                previous_sentence=last_log.user_sentence if last_log else None,
            )
        )

    return session, practice_cards
