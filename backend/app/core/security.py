from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt

from app.core.config import get_settings


def create_magic_token(email: str) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode = {"email": email, "type": "magic", "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_magic_token(token: str) -> str | None:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "magic":
            return None
        return payload.get("email")
    except JWTError:
        return None


def create_access_token(user_id: UUID) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "type": "access", "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> UUID | None:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "access":
            return None
        user_id: str | None = payload.get("sub")
        if user_id is None:
            return None
        return UUID(user_id)
    except (JWTError, ValueError):
        return None
