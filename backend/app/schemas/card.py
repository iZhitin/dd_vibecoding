from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CardCreate(BaseModel):
    word: str
    translation: str
    context_sentence: str | None = None


class CardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    word: str
    translation: str
    context_sentence: str | None = None
    weight: float
    next_review_at: datetime | None = None
    created_at: datetime


class CardList(BaseModel):
    items: list[CardRead]
    total: int
