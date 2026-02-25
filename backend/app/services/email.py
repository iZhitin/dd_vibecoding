import asyncio
import logging

import resend

from app.core.config import get_settings

logger = logging.getLogger(__name__)


async def send_email(to: str, subject: str, html: str) -> bool:
    settings = get_settings()
    
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY is not set. Skipping email sending.")
        return False

    resend.api_key = settings.RESEND_API_KEY

    def _send():
        return resend.Emails.send({
            "from": settings.RESEND_FROM_EMAIL,
            "to": to,
            "subject": subject,
            "html": html,
        })

    max_retries = 2
    base_delay = 1.0

    for attempt in range(max_retries + 1):
        try:
            await asyncio.to_thread(_send)
            logger.info(f"Email sent successfully to {to}")
            return True
        except Exception as e:
            logger.error(f"Error sending email to {to}: {e}")
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                logger.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                logger.error(f"Failed to send email to {to} after {max_retries + 1} attempts")
                
    return False
