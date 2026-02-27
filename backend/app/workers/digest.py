import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.database import async_session_maker
from app.models.practice_log import PracticeLog
from app.models.practice_session import PracticeSession, SessionStatus
from app.models.user import User
from app.services.email import send_digest_email

logger = logging.getLogger(__name__)


async def send_daily_digests(ctx: dict) -> None:
    logger.info("Running digest check")
    settings = get_settings()

    async with async_session_maker() as db:
        # Get all users
        res = await db.execute(select(User))
        users = res.scalars().all()

        utc_now = datetime.now(UTC)

        for user in users:
            try:
                # 1. Check if enough time has passed since last_digest_at
                last_sent = user.last_digest_at
                if last_sent:
                    last_sent = last_sent.replace(tzinfo=UTC)
                    next_allowed = last_sent + timedelta(hours=settings.DIGEST_INTERVAL_HOURS)
                    if utc_now < next_allowed:
                        continue
                
                # 2. Find sessions completed after last_sent (or all completed if never sent)
                sess_stmt = (
                    select(PracticeSession)
                    .options(selectinload(PracticeSession.logs).selectinload(PracticeLog.card))
                    .where(
                        PracticeSession.user_id == user.id,
                        PracticeSession.status == SessionStatus.COMPLETED,
                    )
                )
                if last_sent:
                    sess_stmt = sess_stmt.where(
                        PracticeSession.completed_at > last_sent.replace(tzinfo=None)
                    )
                
                sess_res = await db.execute(sess_stmt)
                all_sessions = list(sess_res.scalars().all())

                if not all_sessions:
                    continue

                # 3. Filter only sessions that are FULLY reviewed by LLM
                target_sessions = []
                reviews = []
                for s in all_sessions:
                    session_ready = True
                    session_reviews = []
                    for log in s.logs:
                        if log.grade is None:
                            session_ready = False
                            break
                        
                        fb = log.llm_feedback or {}
                        session_reviews.append({
                            "grade": log.grade.value,
                            "word": log.card.word,
                            "explanation": fb.get("explanation", ""),
                            "praise": fb.get("praise"),
                            "corrected_sentence": fb.get("corrected_sentence"),
                        })
                    
                    if session_ready and session_reviews:
                        target_sessions.append(s)
                        reviews.extend(session_reviews)

                if not reviews:
                    logger.info(f"No fully reviewed sessions for user {user.id} yet.")
                    continue

                session_id_str = str(target_sessions[-1].id)

                success = await send_digest_email(
                    to=user.email,
                    session_id=session_id_str,
                    reviews=reviews,
                    streak=user.streak_current,
                    app_url=settings.APP_URL,
                )

                if success:
                    # Update to the latest session's completion time or now
                    user.last_digest_at = utc_now.replace(tzinfo=None)
                    await db.commit()
                    logger.info(f"Digest sent to user {user.id} (updated last_digest_at)")

            except Exception as e:
                logger.error(f"Error processing digest for user {user.id}: {e}")
                await db.rollback()
