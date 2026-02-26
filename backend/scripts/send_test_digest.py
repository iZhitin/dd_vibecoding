"""Send a test digest email for the latest completed session."""
import asyncio
import sys

async def main():
    from app.core.config import get_settings
    from app.core.database import async_session_maker
    from app.models.practice_log import PracticeLog
    from app.models.practice_session import PracticeSession, SessionStatus
    from app.models.user import User
    from app.services.email import send_digest_email

    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    settings = get_settings()

    async with async_session_maker() as db:
        # Find the latest completed session with graded logs
        stmt = (
            select(PracticeSession)
            .options(selectinload(PracticeSession.logs).selectinload(PracticeLog.card))
            .where(PracticeSession.status == SessionStatus.COMPLETED)
            .order_by(PracticeSession.completed_at.desc())
            .limit(1)
        )
        res = await db.execute(stmt)
        session = res.scalar_one_or_none()

        if not session:
            print("No completed sessions found.")
            sys.exit(1)

        user = await db.get(User, session.user_id)
        if not user:
            print("User not found.")
            sys.exit(1)

        reviews = []
        for log in session.logs:
            if log.grade is None:
                print(f"Log {log.id} has no grade yet. Run LLM review first.")
                sys.exit(1)
            fb = log.llm_feedback or {}
            reviews.append({
                "grade": log.grade.value,
                "word": log.card.word,
                "explanation": fb.get("explanation", ""),
                "praise": fb.get("praise"),
            })

        print(f"Sending digest for session {session.id} to {user.email}...")
        print(f"  Reviews: {len(reviews)} cards")

        success = await send_digest_email(
            to=user.email,
            session_id=str(session.id),
            reviews=reviews,
            streak=user.streak_current,
            app_url=settings.APP_URL,
        )

        if success:
            print("✅ Digest email sent successfully!")
        else:
            print("❌ Failed to send digest email. Check logs.")

if __name__ == "__main__":
    asyncio.run(main())
