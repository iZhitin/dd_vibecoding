
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.card import CardCreate, CardList, CardRead
from app.services import card as card_service

router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.post("", response_model=CardRead, status_code=status.HTTP_201_CREATED)
async def create_card(
    data: CardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await card_service.create_card(current_user.id, data, db)


@router.get("", response_model=CardList)
async def list_cards(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    items, total = await card_service.get_user_cards(current_user.id, db, offset, limit)
    return CardList(items=list(items), total=total)
