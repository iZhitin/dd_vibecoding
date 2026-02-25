from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.main import app
from app.models.user import User


@pytest.fixture
def current_user():
    return User(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        email="test@example.com",
    )


@pytest.fixture
async def client(current_user):
    app.dependency_overrides[get_current_user] = lambda: current_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_translate_success_deepl(client: AsyncClient):
    # Mock settings to have DEEPL_API_KEY
    settings = get_settings()
    settings.DEEPL_API_KEY = "dummy_fx_key:fx"

    with patch("app.services.translation.httpx.AsyncClient") as mock_client_class:
        from unittest.mock import MagicMock
        mock_instance = mock_client_class.return_value.__aenter__.return_value
        
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "translations": [{"text": "счастливая случайность"}]
        }
        mock_instance.post = AsyncMock(return_value=mock_resp)

        response = await client.post(
            "/api/translate",
            json={"word": "serendipity"},
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["word"] == "serendipity"
    assert data["translation"] == "счастливая случайность"
    
    settings.DEEPL_API_KEY = ""


@pytest.mark.asyncio
async def test_translate_fallback_openai(client: AsyncClient):
    settings = get_settings()
    settings.DEEPL_API_KEY = ""
    settings.OPENAI_API_KEY = "dummy_openai_key"

    with patch(
        "openai.resources.chat.completions.AsyncCompletions.create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value.choices = [
            AsyncMock(message=AsyncMock(content="счастливая случайность"))
        ]

        response = await client.post(
            "/api/translate",
            json={"word": "serendipity"},
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["word"] == "serendipity"
    assert data["translation"] == "счастливая случайность"

    settings.OPENAI_API_KEY = ""


@pytest.mark.asyncio
async def test_translate_failure_null(client: AsyncClient):
    settings = get_settings()
    settings.DEEPL_API_KEY = "dummy:fx"
    settings.OPENAI_API_KEY = "dummy_openai"

    with patch("app.services.translation.httpx.AsyncClient") as mock_client_class, \
         patch(
             "openai.resources.chat.completions.AsyncCompletions.create", new_callable=AsyncMock
         ) as mock_create:
        
        mock_instance = mock_client_class.return_value.__aenter__.return_value
        mock_instance.post = AsyncMock(side_effect=Exception("Timeout"))

        mock_create.side_effect = Exception("Timeout")

        response = await client.post(
            "/api/translate",
            json={"word": "serendipity"},
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["translation"] is None

    settings.DEEPL_API_KEY = ""
    settings.OPENAI_API_KEY = ""
