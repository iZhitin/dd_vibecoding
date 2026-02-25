from uuid import UUID

from pydantic import BaseModel, ValidationInfo, field_validator

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
    user_sentence: str
    revealed_translation: bool = False


class PracticeSubmitRequest(BaseModel):
    session_id: UUID
    sentences: list[SentenceSubmit]

    @field_validator("sentences")
    @classmethod
    def check_sentences_length(
        cls, v: list[SentenceSubmit], info: ValidationInfo
    ) -> list[SentenceSubmit]:
        if len(v) != 10:
            raise ValueError("Exactly 10 sentences are required")
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
