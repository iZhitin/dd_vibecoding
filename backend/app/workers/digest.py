import logging
import zoneinfo
from datetime import UTC, datetime, timedelta

from arq.connections import ArqRedis
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.database import async_sessionmaker
from app.models.practice_log import PracticeLog
from app.models.practice_session import PracticeSession, SessionStatus
from app.models.user import User
from app.services.email import send_digest_email

logger = logging.getLogger(__name__)


async def send_daily_digests(ctx: dict) -> None:
    logger.info("Running daily digest check")
    redis: ArqRedis = ctx.get("redis")
    settings = get_settings()

    async with async_sessionmaker() as db:
        stmt = select(User).where(User.timezone.is_not(None))
        res = await db.execute(stmt)
        users = res.scalars().all()

        utc_now = datetime.now(UTC)

        for user in users:
            try:
                user_tz = zoneinfo.ZoneInfo(user.timezone)
                user_now = utc_now.astimezone(user_tz)

                if user_now.hour == 8:
                    cache_key = f"digest_sent:{user.id}:{user_now.date().isoformat()}"
                    if redis:
                        already_sent = await redis.get(cache_key)
                        if already_sent:
                            continue

                    yesterday_local = user_now.date() - timedelta(days=1)
                    
                    sess_stmt = select(PracticeSession).options(
                        selectinload(PracticeSession.logs).selectinload(PracticeLog.card)
                    ).where(
                        PracticeSession.user_id == user.id,
                        PracticeSession.status == SessionStatus.COMPLETED,
                        PracticeSession.completed_at.is_not(None)
                    )
                    sess_res = await db.execute(sess_stmt)
                    sessions = sess_res.scalars().all()
                    
                    target_sessions = []
                    for s in sessions:
                        comp_utc = s.completed_at.replace(tzinfo=UTC)
                        comp_local = comp_utc.astimezone(user_tz)
                        if comp_local.date() == yesterday_local:
                            target_sessions.append(s)
                            
                    if not target_sessions:
                        continue
                        
                    reviews = []
                    all_llm_completed = True
                    for s in target_sessions:
                        for log in s.logs:
                            if log.grade is None:
                                all_llm_completed = False
                                break
                            
                            fb = log.llm_feedback or {}
                            reviews.append({
                                "grade": log.grade.value,
                                "word": log.card.word,
                                "explanation": fb.get("explanation", ""),
                                "praise": fb.get("praise"),
                                "corrected_sentence": fb.get("corrected_sentence"),
                            })
                        if not all_llm_completed:
                            break
                            
                    if not all_llm_completed:
                        logger.warning(
                            f"Skipping digest for user {user.id}, LLM review not finished"
                        )
                        continue
                        
                    if not reviews:
                        continue
                        
                    session_id_str = str(target_sessions[-1].id)
                    
                    success = await send_digest_email(
                        to=user.email,
                        session_id=session_id_str,
                        reviews=reviews,
                        streak=user.streak_current,
                        app_url=settings.APP_URL
                    )
                    
                    if success and redis:
                        await redis.setex(cache_key, 86400, "1")
                        logger.info(f"Daily digest sent to user {user.id}")
                            
            except Exception as e:
                logger.error(f"Error processing digest for user {user.id}: {e}")
