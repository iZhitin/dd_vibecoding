import factory
import datetime
from uuid import uuid4

from app.models.user import User
from app.models.card import Card
from app.models.practice_session import PracticeSession, SessionStatus
from app.models.practice_log import PracticeLog, Grade

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    email = factory.Sequence(lambda n: f"testuser{n}@example.com")
    timezone = "Europe/Moscow"
    streak_current = 0
    streak_frozen_count = 0
    created_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))
    updated_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))

class CardFactory(factory.Factory):
    class Meta:
        model = Card

    id = factory.LazyFunction(uuid4)
    user_id = factory.SelfAttribute('user.id')
    word = factory.Sequence(lambda n: f"word{n}")
    translation = factory.Sequence(lambda n: f"translation{n}")
    context_sentence = "Context sentence example."
    weight = 1.0
    next_review_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))
    created_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))
    updated_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))

class PracticeSessionFactory(factory.Factory):
    class Meta:
        model = PracticeSession

    id = factory.LazyFunction(uuid4)
    user_id = factory.SelfAttribute('user.id')
    status = SessionStatus.ACTIVE
    started_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))
    created_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))
    updated_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))

class PracticeLogFactory(factory.Factory):
    class Meta:
        model = PracticeLog

    id = factory.LazyFunction(uuid4)
    session_id = factory.SelfAttribute('session.id')
    card_id = factory.SelfAttribute('card.id')
    user_sentence = "User sentence example."
    revealed_translation = False
    created_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))
    updated_at = factory.LazyFunction(lambda: datetime.datetime.now(datetime.UTC))
