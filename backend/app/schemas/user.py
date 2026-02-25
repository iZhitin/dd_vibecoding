from datetime import datetime
from uuid import UUID
from zoneinfo import available_timezones

from pydantic import BaseModel, ValidationInfo, field_validator


class UserRead(BaseModel):
    id: UUID
    email: str
    timezone: str | None = None
    streak_current: int
    streak_frozen_count: int
    last_practice_at: datetime | None = None


class TimezoneUpdate(BaseModel):
    timezone: str

    @field_validator("timezone")
    @classmethod
    def check_valid_timezone(cls, v: str, info: ValidationInfo) -> str:
        if v not in available_timezones():
            raise ValueError(f"Invalid timezone: {v}")
        return v
