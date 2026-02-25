import random
import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import Card
from app.models.practice_log import Grade

WEIGHT_REVEALED = 2.0
WEIGHT_RED = 1.5
WEIGHT_YELLOW = 1.2
WEIGHT_GREEN = 0.7
WEIGHT_GREEN_STAR = 0.5
MIN_WEIGHT = 0.01


async def select_practice_cards(
    user_id: uuid.UUID, db: AsyncSession, count: int = 10
) -> Sequence[Card]:
    """Select 'count' practice cards for the given user, based on their weight."""
    stmt = select(Card).where(Card.user_id == user_id, Card.weight > 0)
    result = await db.execute(stmt)
    cards = result.scalars().all()

    if not cards:
        return []

    if len(cards) <= count:
        return cards

    selected_cards = []
    pool = list(cards)
    pool_weights = [c.weight for c in pool]

    for _ in range(count):
        if not pool:
            break
        # Choose 1 index based on the remaining weights
        chosen_idx = random.choices(range(len(pool)), weights=pool_weights, k=1)[0]
        selected_cards.append(pool[chosen_idx])
        pool.pop(chosen_idx)
        pool_weights.pop(chosen_idx)

    return selected_cards


def update_weight_after_review(card: Card, grade: Grade, revealed: bool) -> None:
    """Update learning weight based on the review outcome."""
    if revealed:
        card.weight *= WEIGHT_REVEALED

    if grade == Grade.RED:
        card.weight *= WEIGHT_RED
    elif grade == Grade.YELLOW:
        card.weight *= WEIGHT_YELLOW
    elif grade == Grade.GREEN:
        card.weight *= WEIGHT_GREEN
    elif grade == Grade.GREEN_STAR:
        card.weight *= WEIGHT_GREEN_STAR

    card.weight = max(card.weight, MIN_WEIGHT)


def update_weight_after_reveal(card: Card) -> None:
    """Increase weight when translation is revealed without giving an answer."""
    card.weight *= WEIGHT_REVEALED
