import uuid
from datetime import datetime, time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .card import Card
    from .practice_session import PracticeSession

from sqlalchemy import Boolean, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    timezone: Mapped[str | None] = mapped_column(String, nullable=True)
    avg_practice_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    streak_current: Mapped[int] = mapped_column(Integer, default=0)
    streak_frozen_count: Mapped[int] = mapped_column(Integer, default=0)
    last_practice_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_digest_at: Mapped[datetime | None] = mapped_column(nullable=True)
    is_frozen: Mapped[bool] = mapped_column(Boolean, default=False)

    cards: Mapped[list["Card"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[list["PracticeSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
