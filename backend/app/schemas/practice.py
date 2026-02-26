from uuid import UUID

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from app.core.sanitize import sanitize_text
from app.models.practice_log import Grade
from app.schemas.llm import SentenceReview


class PracticeCardRead(BaseModel):
    card_id: UUID
    word: str
    context_sentence: str | None = None
    previous_sentence: str | None = None


class DailyPracticeResponse(BaseModel):
    session_id: UUID
    cards: list[PracticeCardRead]


class SentenceSubmit(BaseModel):
    card_id: UUID
    user_sentence: str = Field(..., max_length=1000)
    revealed_translation: bool = False

    @field_validator("user_sentence", mode="before")
    @classmethod
    def validate_user_sentence(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        v = sanitize_text(v)
        if not v:
            raise ValueError("Sentence cannot be empty")
        return v


class PracticeSubmitRequest(BaseModel):
    session_id: UUID
    sentences: list[SentenceSubmit]

    @field_validator("sentences")
    @classmethod
    def check_sentences_length(
        cls, v: list[SentenceSubmit], info: ValidationInfo
    ) -> list[SentenceSubmit]:
        if len(v) < 1:
            raise ValueError("At least one sentence is required")
        return v


class PracticeLogReview(BaseModel):
    id: UUID
    card_word: str
    user_sentence: str
    grade: Grade | None = None
    llm_feedback: SentenceReview | None = None


class PracticeSessionReviewResponse(BaseModel):
    session_id: UUID
    logs: list[PracticeLogReview]
