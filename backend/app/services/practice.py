import logging
import uuid
from datetime import UTC, datetime

from arq import create_pool
from arq.connections import ArqRedis, RedisSettings
from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.card import Card
from app.models.practice_log import PracticeLog
from app.models.practice_session import PracticeSession, SessionStatus
from app.models.user import User
from app.schemas.practice import PracticeCardRead, PracticeSubmitRequest
from app.services.srs import select_practice_cards, update_weight_after_reveal
from app.services.streak import update_streak

logger = logging.getLogger(__name__)

_pool: ArqRedis | None = None

async def get_arq_pool() -> ArqRedis:
    global _pool
    if _pool is None:
        settings = get_settings()
        _pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
    return _pool


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
    card_ids = [card.id for card in cards]

    last_logs_dict: dict[uuid.UUID, PracticeLog] = {}
    if card_ids:
        # PostgreSQL specific distinct ON
        logs_stmt = (
            select(PracticeLog)
            .where(PracticeLog.card_id.in_(card_ids))
            .distinct(PracticeLog.card_id)
            .order_by(PracticeLog.card_id, desc(PracticeLog.created_at))
        )
        logs_res = await db.execute(logs_stmt)
        for log in logs_res.scalars().all():
            last_logs_dict[log.card_id] = log

    practice_cards: list[PracticeCardRead] = []
    for card in cards:
        last_log = last_logs_dict.get(card.id)
        practice_cards.append(
            PracticeCardRead(
                card_id=card.id,
                word=card.word,
                context_sentence=card.context_sentence,
                previous_sentence=last_log.user_sentence if last_log else None,
            )
        )

    return session, practice_cards


async def submit_practice(
    user_id: uuid.UUID, data: PracticeSubmitRequest, db: AsyncSession
) -> PracticeSession:
    stmt = select(PracticeSession).where(
        PracticeSession.id == data.session_id,
    )
    result = await db.execute(stmt)
    session = result.scalars().first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to submit this session")
    if session.status != SessionStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Session is not active")

    card_ids = [sentence.card_id for sentence in data.sentences]
    
    # Bulk load cards
    cards_stmt = select(Card).where(Card.id.in_(card_ids))
    cards_res = await db.execute(cards_stmt)
    cards_dict = {c.id: c for c in cards_res.scalars().all()}
    
    # Bulk load last logs
    last_logs_dict: dict[uuid.UUID, PracticeLog] = {}
    if card_ids:
        logs_stmt = (
            select(PracticeLog)
            .where(PracticeLog.card_id.in_(card_ids))
            .distinct(PracticeLog.card_id)
            .order_by(PracticeLog.card_id, desc(PracticeLog.created_at))
        )
        logs_res = await db.execute(logs_stmt)
        for log in logs_res.scalars().all():
            last_logs_dict[log.card_id] = log

    for sentence in data.sentences:
        card = cards_dict.get(sentence.card_id)
        if not card or card.user_id != user_id:
            raise HTTPException(
                status_code=403, detail=f"Not authorized to submit for card {sentence.card_id}"
            )

        last_log = last_logs_dict.get(card.id)
        if last_log and last_log.user_sentence == sentence.user_sentence:
            logger.info("Soft-check: User copy-pasted previous sentence for card %s", card.id)

        log = PracticeLog(
            session_id=session.id,
            card_id=card.id,
            user_sentence=sentence.user_sentence,
            revealed_translation=sentence.revealed_translation,
            grade=None,
            llm_feedback=None,
        )
        db.add(log)

        if sentence.revealed_translation:
            update_weight_after_reveal(card)

    session.status = SessionStatus.COMPLETED
    session.completed_at = datetime.now(UTC)

    user_stmt = select(User).where(User.id == user_id)
    user_res = await db.execute(user_stmt)
    user = user_res.scalars().first()
    if user:
        await update_streak(user, db)

        if user.timezone:
            import zoneinfo
            user_tz = zoneinfo.ZoneInfo(user.timezone)
            now_local = datetime.now(UTC).astimezone(user_tz)
            user.avg_practice_time = now_local.time()

    await db.commit()
    await db.refresh(session)

    pool = await get_arq_pool()
    await pool.enqueue_job("review_sentences", session.id)

    return session
