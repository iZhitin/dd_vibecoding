import logging
import zoneinfo
from datetime import UTC, datetime

from arq.connections import ArqRedis
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.user import User
from app.services.email import send_reminder_email

logger = logging.getLogger(__name__)


async def smart_nudge_check(ctx: dict) -> None:
    logger.info("Running smart nudge check")
    redis: ArqRedis = ctx["redis"]

    async with async_session_maker() as db:
        stmt = select(User).where(
            User.avg_practice_time.is_not(None), User.timezone.is_not(None)
        )
        res = await db.execute(stmt)
        users = res.scalars().all()

        utc_now = datetime.now(UTC)

        for user in users:
            try:
                user_tz = zoneinfo.ZoneInfo(user.timezone)
                user_now = utc_now.astimezone(user_tz)

                if user.last_practice_at:
                    last_practice = user.last_practice_at.astimezone(user_tz)
                    if last_practice.date() == user_now.date():
                        continue  # Already practiced today

                avg_time = user.avg_practice_time
                nudge_hour = (avg_time.hour + 1) % 24

                # Check if current hour in user's timezone matches nudge hour
                if user_now.hour == nudge_hour:
                    cache_key = f"nudge_sent:{user.id}:{user_now.date().isoformat()}"
                    already_sent = await redis.get(cache_key)
                    if already_sent:
                        continue

                    # Attempt to send email
                    success = await send_reminder_email(user.email, card_count=10)
                    if success:
                        await redis.setex(cache_key, 86400, "1")  # TTL 24h
                        logger.info(f"Smart nudge sent to user {user.id}")

            except Exception as e:
                logger.error(f"Error processing nudge for user {user.id}: {e}")
