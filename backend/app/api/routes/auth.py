from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, VerifyRequest
from app.services.auth import request_magic_link, verify_magic_link

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):  # noqa: B008
    return await request_magic_link(request.email, db)


@router.post("/verify", response_model=TokenResponse)
async def verify(request: VerifyRequest, db: AsyncSession = Depends(get_db)):  # noqa: B008
    token_response = await verify_magic_link(request.token, db)
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired magic token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_response
