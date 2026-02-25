from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CardBase(BaseModel):
    word: str
    translation: str
    context_sentence: str | None = None


class CardCreate(CardBase):
    pass


class CardRead(CardBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    weight: float
    next_review_at: datetime | None = None
    created_at: datetime


class CardList(BaseModel):
    items: list[CardRead]
    total: int


class CardTranslationRead(BaseModel):
    card_id: UUID
    translation: str
