from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.schemas.auth import LoginRequest, TokenResponse, VerifyRequest
from app.services.auth import request_magic_link, verify_magic_link

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(
    request: Request, login_req: LoginRequest, db: AsyncSession = Depends(get_db)  # noqa: B008
):
    return await request_magic_link(login_req.email, db)


@router.post("/verify", response_model=TokenResponse)
async def verify(verify_req: VerifyRequest, db: AsyncSession = Depends(get_db)):  # noqa: B008
    token_response = await verify_magic_link(verify_req.token, db)
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired magic token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_response
