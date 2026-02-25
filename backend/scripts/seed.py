import asyncio
import random
from datetime import UTC, datetime, time, timedelta

from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.card import Card
from app.models.practice_log import Grade, PracticeLog
from app.models.practice_session import PracticeSession, SessionStatus
from app.models.user import User

WORDS = [
    ("serendipity", "счастливая случайность", "We found this great restaurant by pure serendipity."),
    ("ephemeral", "эфемерный, недолговечный", "Fame in the world of rock and roll is largely ephemeral."),
    ("ubiquitous", "вездесущий", "His ubiquitous influence was felt by all the family."),
    ("eloquent", "красноречивый", "She made an eloquent appeal for action."),
    ("lucid", "ясный, понятный", "He gave a very lucid account of the events."),
    ("resilient", "жизнестойкий", "Babies are generally far more resilient than new parents realize."),
    ("meticulous", "тщательный, дотошный", "Many hours of meticulous preparation have gone into writing the book."),
    ("pragmatic", "прагматичный", "In business, the pragmatic approach to problems is often more successful than an idealistic one."),
    ("nostalgia", "ностальгия", "Some people feel nostalgia for their schooldays."),
    ("paradigm", "парадигма", "Some of these educators are hoping to produce a change in the current cultural paradigm."),
    ("profound", "глубокий, основательный", "His mother's death when he was aged six had a very profound effect on him."),
    ("ambiguous", "двусмысленный", "His reply to my question was somewhat ambiguous."),
    ("candid", "искренний, откровенный", "The two presidents have had candid talks about the current crisis."),
    ("inevitable", "неизбежный", "The accident was the inevitable consequence/result/outcome of carelessness."),
    ("vulnerable", "уязвимый", "I felt very vulnerable, standing there without any clothes on.")
]


async def seed() -> None:
    print("Starting database seed...")
    async with async_session_maker() as session:
        # Check if user already exists
        stmt = select(User).where(User.email == "test@dd.local")
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            print("User test@dd.local already exists. Deleting user for clean seed...")
            await session.delete(user)
            await session.commit()
            print("Deleted existing test user.")

        print("Creating User...")
        user = User(
            email="test@dd.local",
            timezone="Europe/Moscow",
            streak_current=5,
            streak_frozen_count=0,
            avg_practice_time=time(9, 0)
        )
        session.add(user)
        # Flush to get user id
        await session.flush()
        
        print("Creating 15 Cards...")
        now = datetime.now(UTC).replace(tzinfo=None)
        cards = []
        for i, (word, translation, context) in enumerate(WORDS):
            # weights from 0.1 to 2.0
            weight = 0.1 + (1.9 * i / max(1, len(WORDS) - 1))
            
            # spread next review times around now (-48 to +48 hours)
            offset_hours = random.randint(-48, 48)
            next_review_at = now + timedelta(hours=offset_hours)
            
            card = Card(
                user_id=user.id,
                word=word,
                translation=translation,
                context_sentence=context,
                weight=round(weight, 3),
                next_review_at=next_review_at
            )
            cards.append(card)
            session.add(card)
            
        await session.flush()
        
        print("Creating 2 Practice Sessions with 10 Logs each...")
        grades = [Grade.GREEN, Grade.GREEN_STAR, Grade.YELLOW, Grade.RED]
        
        for s_idx in range(2):
            session_start = now - timedelta(days=s_idx + 1)
            p_session = PracticeSession(
                user_id=user.id,
                started_at=session_start,
                completed_at=session_start + timedelta(minutes=10),
                status=SessionStatus.COMPLETED
            )
            session.add(p_session)
            await session.flush()
            
            # Create 10 logs for each session (select random cards)
            session_cards = random.sample(cards, 10)
            for card in session_cards:
                log = PracticeLog(
                    session_id=p_session.id,
                    card_id=card.id,
                    user_sentence=f"This is a mocked sentence for word: {card.word}",
                    grade=random.choice(grades),
                    llm_feedback={
                        "issue": "None", 
                        "explanation": "Perfectly fine."
                    } if random.random() > 0.5 else None,
                    revealed_translation=random.choice([True, False])
                )
                session.add(log)
        
        await session.commit()
        print("Seed completed successfully!")
        print("Created: 1 User, 15 Cards, 2 Sessions, 20 Logs.")

def main() -> None:
    asyncio.run(seed())

if __name__ == "__main__":
    main()
