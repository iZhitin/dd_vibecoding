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


async def send_magic_link_email(to: str, url: str) -> bool:
    from app.templates.emails import MAGIC_LINK_HTML

    html = MAGIC_LINK_HTML.format(url=url)
    return await send_email(
        to=to,
        subject="DD — Your Login Link",
        html=html
    )


async def send_reminder_email(to: str, card_count: int) -> bool:
    from app.core.config import get_settings
    from app.templates.emails import REMINDER_HTML

    settings = get_settings()
    html = REMINDER_HTML.format(card_count=card_count, app_url=settings.APP_URL)
    return await send_email(
        to=to,
        subject="Time to practice",
        html=html
    )


async def send_digest_email(
    to: str, session_id: str, reviews: list[dict], streak: int, app_url: str
) -> bool:
    from app.templates.emails import DAILY_DIGEST_HTML_WRAPPER, REVIEW_ITEM_HTML

    reviews_html = ""
    for r in reviews:
        praise_html = f'<div class="praise">{r.get("praise")}</div>' if r.get("praise") else ""
        reviews_html += REVIEW_ITEM_HTML.format(
            grade=r.get("grade", "GREEN"),
            word=r.get("word", ""),
            praise_html=praise_html,
            feedback=r.get("explanation", r.get("feedback", ""))
        )

    html = DAILY_DIGEST_HTML_WRAPPER.format(
        streak=streak,
        session_id=session_id,
        app_url=app_url,
        reviews_html=reviews_html,
    )

    return await send_email(
        to=to,
        subject="Your Daily Digest",
        html=html
    )
