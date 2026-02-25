from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.translate import TranslateRequest, TranslateResponse
from app.services.translation import translate_word

router = APIRouter(prefix="/api/translate", tags=["translation"])

@router.post("", response_model=TranslateResponse)
async def translate_word_endpoint(
    req: TranslateRequest,
    current_user: User = Depends(get_current_user)
):
    translation = await translate_word(req.word)
    return TranslateResponse(word=req.word, translation=translation)
