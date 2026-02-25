import enum
import uuid
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .card import Card
    from .practice_session import PracticeSession

from sqlalchemy import Boolean, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Grade(enum.StrEnum):
    GREEN = "GREEN"
    GREEN_STAR = "GREEN_STAR"
    YELLOW = "YELLOW"
    RED = "RED"


class PracticeLog(TimestampMixin, Base):
    __tablename__ = "practice_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("practice_sessions.id", ondelete="CASCADE")
    )
    card_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cards.id", ondelete="CASCADE"))
    user_sentence: Mapped[str] = mapped_column(Text)
    grade: Mapped[Grade | None] = mapped_column(Enum(Grade), nullable=True)
    llm_feedback: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    revealed_translation: Mapped[bool] = mapped_column(Boolean, default=False)

    session: Mapped["PracticeSession"] = relationship(back_populates="logs")
    card: Mapped["Card"] = relationship(back_populates="logs")
