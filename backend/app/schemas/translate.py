from pydantic import BaseModel


class TranslateRequest(BaseModel):
    word: str


class TranslateResponse(BaseModel):
    word: str
    translation: str | None
