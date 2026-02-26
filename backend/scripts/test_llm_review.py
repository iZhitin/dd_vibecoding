"""
Test LLM review for a practice session — runs directly (no Arq/Redis needed).

Usage:
    cd backend
    python -m scripts.test_llm_review              # review last ungraded session
    python -m scripts.test_llm_review <session_id>  # review specific session
    python -m scripts.test_llm_review --force <id>   # re-review even if already graded
"""

import asyncio
import sys
import uuid

from sqlalchemy import desc, func, select
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.database import async_session_maker
from app.models.practice_log import PracticeLog
from app.models.practice_session import PracticeSession, SessionStatus
from app.workers.llm_review import review_sentences


GRADE_COLORS = {
    "GREEN": "\033[92m",       # bright green
    "GREEN_STAR": "\033[92m⭐", # green + star
    "YELLOW": "\033[93m",      # yellow
    "RED": "\033[91m",         # red
}
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


def print_header(text: str) -> None:
    print(f"\n{BOLD}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{RESET}\n")


def print_review(index: int, log: PracticeLog) -> None:
    """Pretty-print a single reviewed sentence."""
    word = log.card.word if log.card else "???"
    grade = log.grade.value if log.grade else "PENDING"
    color = GRADE_COLORS.get(grade, "")

    print(f"{BOLD}[{index}] Word: {word}{RESET}")
    print(f"    Sentence: {log.user_sentence}")
    print(f"    Grade:    {color}{grade}{RESET}")

    if log.llm_feedback:
        explanation = log.llm_feedback.get("explanation", "")
        corrected = log.llm_feedback.get("corrected_sentence", "")
        praise = log.llm_feedback.get("praise", "")

        if explanation:
            print(f"    Feedback: {explanation}")
        if corrected:
            print(f"    Correct:  {DIM}{corrected}{RESET}")
        if praise:
            print(f"    Praise:   {praise}")
    print()


async def find_session(session_id: uuid.UUID | None, force: bool) -> uuid.UUID | None:
    """Find a session to review: specific ID, or the latest ungraded one."""
    async with async_session_maker() as db:
        if session_id:
            session = await db.get(PracticeSession, session_id)
            if not session:
                print(f"\033[91mSession {session_id} not found{RESET}")
                return None
            print(f"Found session: {session.id} (status={session.status})")
            return session.id

        # Find latest completed session with ungraded logs
        subq = (
            select(PracticeLog.session_id)
            .where(PracticeLog.grade.is_(None))
            .distinct()
            .subquery()
        )
        stmt = (
            select(PracticeSession)
            .where(
                PracticeSession.status == SessionStatus.COMPLETED,
                PracticeSession.id.in_(select(subq)),
            )
            .order_by(desc(PracticeSession.completed_at))
            .limit(1)
        )
        result = await db.execute(stmt)
        session = result.scalars().first()

        if session:
            print(f"Found ungraded session: {session.id}")
            print(f"  Completed at: {session.completed_at}")
            return session.id

        if force:
            # Fallback: take the latest completed session
            stmt2 = (
                select(PracticeSession)
                .where(PracticeSession.status == SessionStatus.COMPLETED)
                .order_by(desc(PracticeSession.completed_at))
                .limit(1)
            )
            result2 = await db.execute(stmt2)
            session2 = result2.scalars().first()
            if session2:
                print(f"Re-reviewing already graded session: {session2.id}")
                return session2.id

        # No completed sessions — show what exists
        count_stmt = select(func.count()).select_from(PracticeSession)
        total = (await db.execute(count_stmt)).scalar()

        active_stmt = (
            select(PracticeSession)
            .where(PracticeSession.status == SessionStatus.ACTIVE)
            .order_by(desc(PracticeSession.started_at))
        )
        active_res = await db.execute(active_stmt)
        active_sessions = active_res.scalars().all()

        print(f"\033[93mNo completed ungraded sessions found.{RESET}")
        print(f"Total sessions in DB: {total}")
        if active_sessions:
            print("Active (not submitted) sessions:")
            for s in active_sessions:
                print(f"  - {s.id} started at {s.started_at}")
            print(
                f"\n{DIM}Hint: Complete a practice session through the UI "
                f"(POST /api/practice/submit), then re-run this script.{RESET}"
            )
        return None


async def show_results(session_id: uuid.UUID) -> None:
    """Load and display review results from DB."""
    async with async_session_maker() as db:
        stmt = (
            select(PracticeLog)
            .where(PracticeLog.session_id == session_id)
            .options(selectinload(PracticeLog.card))
            .order_by(PracticeLog.created_at)
        )
        result = await db.execute(stmt)
        logs = list(result.scalars().all())

        if not logs:
            print("No logs found for this session.")
            return

        print_header("AI Review Results")

        graded = sum(1 for log in logs if log.grade is not None)
        total = len(logs)

        for i, log in enumerate(logs, 1):
            print_review(i, log)

        # Summary
        if graded > 0:
            grade_counts: dict[str, int] = {}
            for log in logs:
                if log.grade:
                    g = log.grade.value
                    grade_counts[g] = grade_counts.get(g, 0) + 1

            print_header("Summary")
            print(f"  Graded: {graded}/{total}")
            for grade, count in sorted(grade_counts.items()):
                color = GRADE_COLORS.get(grade, "")
                print(f"  {color}{grade}: {count}{RESET}")
        else:
            print(f"{DIM}  (no grades yet — review may not have run){RESET}")


async def main() -> None:
    settings = get_settings()

    # Parse CLI args
    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--force"]
    session_id = uuid.UUID(args[0]) if args else None

    # Preflight checks
    if not settings.OPENROUTER_API_KEY:
        print(
            f"\033[91mOPENROUTER_API_KEY is not set in .env — "
            f"AI review will be skipped!{RESET}"
        )
        print("Set it and re-run.\n")
        return

    print(f"{DIM}Model: {settings.LLM_MODEL}{RESET}")
    print(f"{DIM}OpenRouter URL: {settings.OPENROUTER_URL}{RESET}\n")

    # Find session
    target_id = await find_session(session_id, force)
    if not target_id:
        return

    # Run review directly (no Arq)
    print(f"\n⏳ Running AI review for session {target_id}...")
    await review_sentences(ctx={}, session_id=target_id)
    print("✅ Review complete!\n")

    # Show results
    await show_results(target_id)


if __name__ == "__main__":
    asyncio.run(main())
