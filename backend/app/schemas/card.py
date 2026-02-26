import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.sanitize import sanitize_text


class CardBase(BaseModel):
    word: str = Field(..., max_length=100)
    translation: str = Field(..., max_length=500)
    context_sentence: str | None = Field(None, max_length=1000)

    @field_validator("word", mode="before")
    @classmethod
    def validate_word(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        v = sanitize_text(v)
        if not v:
            raise ValueError("Word cannot be empty")
        if not re.match(r"^[\w\s-]+$", v, re.UNICODE):
            raise ValueError("Word contains invalid characters")
        return v

    @field_validator("translation", mode="before")
    @classmethod
    def validate_translation(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        v = sanitize_text(v)
        if not v:
            raise ValueError("Translation cannot be empty")
        return v

    @field_validator("context_sentence", mode="before")
    @classmethod
    def validate_context_sentence(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = sanitize_text(v)
        if not v:
            return None
        return v

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
