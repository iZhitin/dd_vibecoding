import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import create_access_token, create_magic_token, verify_magic_token
from app.models.user import User
from app.schemas.auth import TokenResponse

logger = logging.getLogger(__name__)


async def request_magic_link(email: str, db: AsyncSession) -> dict[str, str]:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        user = User(email=email)
        db.add(user)
        await db.commit()
    
    token = create_magic_token(email)
    settings = get_settings()
    url = f"{settings.APP_URL}/auth/verify?token={token}"
    
    from app.services.email import send_magic_link_email, mask_email
    await send_magic_link_email(
        to=email,
        url=url
    )
    
    logger.info(f"Magic link for {mask_email(email)} sent")
    
    return {"message": "Magic link sent"}


async def verify_magic_link(token: str, db: AsyncSession) -> TokenResponse | None:
    email = verify_magic_token(token)
    if not email:
        return None
        
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
        
    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)
