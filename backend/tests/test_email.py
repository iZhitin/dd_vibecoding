from unittest.mock import patch

import pytest

from app.core.config import get_settings
from app.services.email import send_email


@pytest.fixture
def mock_settings():
    settings = get_settings()
    settings.RESEND_API_KEY = "test_key"
    settings.RESEND_FROM_EMAIL = "test@example.com"
    return settings


@pytest.mark.asyncio
async def test_send_email_success(mock_settings):
    with patch("app.services.email.get_settings", return_value=mock_settings), \
         patch("resend.Emails.send") as mock_send:
        mock_send.return_value = {"id": "123"}
        result = await send_email("user@test.com", "Subj", "<p>html</p>")
        assert result is True
        mock_send.assert_called_once()


@pytest.mark.asyncio
async def test_send_email_no_api_key():
    settings = get_settings()
    settings.RESEND_API_KEY = ""
    with patch("app.services.email.get_settings", return_value=settings), \
         patch("resend.Emails.send") as mock_send:
        result = await send_email("user@test.com", "Subj", "<p>html</p>")
        assert result is False
        mock_send.assert_not_called()


@pytest.mark.asyncio
async def test_send_email_retry_failure(mock_settings):
    with patch("app.services.email.get_settings", return_value=mock_settings), \
         patch("resend.Emails.send") as mock_send, \
         patch("asyncio.sleep") as mock_sleep:
        mock_send.side_effect = Exception("API error")
        result = await send_email("user@test.com", "Subj", "<p>html</p>")
        assert result is False
        assert mock_send.call_count == 3  # Initial + 2 retries
        assert mock_sleep.call_count == 2
