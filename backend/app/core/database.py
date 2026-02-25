import sys
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

# Avoid echoing SQL in tests to reduce noise, though usually it's config-driven
is_test = "pytest" in sys.modules
engine = create_async_engine(
    get_settings().DATABASE_URL,
    echo=not is_test,
)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting an async database session per request.
    Handles commit on success and rollback on exception.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
