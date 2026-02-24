from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://dd:dd@localhost:5432/dd"
    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080

    OPENAI_API_KEY: str = ""
    DEEPL_API_KEY: str = ""

    RESEND_API_KEY: str = ""
    RESEND_FROM_EMAIL: str = "dd@yourdomain.com"

    APP_URL: str = "http://localhost:5173"
    APP_ENV: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

