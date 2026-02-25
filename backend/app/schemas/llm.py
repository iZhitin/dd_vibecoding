from pydantic import BaseModel

from app.models.practice_log import Grade


class SentenceReview(BaseModel):
    grade: Grade
    corrected_sentence: str | None = None
    explanation: str
    praise: str | None = None


class SessionReviewResponse(BaseModel):
    reviews: list[SentenceReview]
