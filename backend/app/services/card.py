from collections.abc import Sequence
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import Card
from app.schemas.card import CardCreate


async def create_card(user_id: UUID, data: CardCreate, db: AsyncSession) -> Card:
    card = Card(
        user_id=user_id,
        word=data.word,
        translation=data.translation,
        context_sentence=data.context_sentence,
        weight=1.0,
        next_review_at=datetime.now(timezone.utc),
    )
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card


async def get_user_cards(
    user_id: UUID, db: AsyncSession, offset: int = 0, limit: int = 50
) -> tuple[Sequence[Card], int]:
    # Get total count
    count_stmt = select(func.count()).select_from(Card).where(Card.user_id == user_id)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    # Get items
    stmt = (
        select(Card)
        .where(Card.user_id == user_id)
        .order_by(Card.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    items = result.scalars().all()

    return items, total
