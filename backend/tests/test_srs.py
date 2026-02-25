import uuid
from unittest.mock import AsyncMock

import pytest

from app.models.card import Card
from app.models.practice_log import Grade
from app.services.srs import (
    select_practice_cards,
    update_weight_after_reveal,
    update_weight_after_review,
)


@pytest.fixture
def mock_db():
    db = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_select_practice_cards_returns_10_or_less(mock_db):
    user_id = uuid.uuid4()
    
    # Create 15 dummy cards
    cards = [Card(id=uuid.uuid4(), weight=1.0) for _ in range(15)]
    
    class MockResult:
        def scalars(self):
            class MockItems:
                def all(self):
                    return cards
            return MockItems()
            
    mock_db.execute.return_value = MockResult()

    selected = await select_practice_cards(user_id, mock_db, count=10)
    assert len(selected) == 10

    # Ensure no duplicates
    selected_ids = [c.id for c in selected]
    assert len(set(selected_ids)) == 10


@pytest.mark.asyncio
async def test_select_practice_cards_less_than_count(mock_db):
    user_id = uuid.uuid4()
    
    # Create only 5 dummy cards
    cards = [Card(id=uuid.uuid4(), weight=1.0) for _ in range(5)]
    
    class MockResult:
        def scalars(self):
            class MockItems:
                def all(self):
                    return cards
            return MockItems()
            
    mock_db.execute.return_value = MockResult()

    selected = await select_practice_cards(user_id, mock_db, count=10)
    assert len(selected) == 5


@pytest.mark.asyncio
async def test_select_practice_cards_statistical_distribution(mock_db):
    user_id = uuid.uuid4()
    
    # 2 cards with different weights
    card1 = Card(id=uuid.uuid4(), weight=9.0)   # 90% probability initially
    card2 = Card(id=uuid.uuid4(), weight=1.0)   # 10% probability initially
    
    class MockResult:
        def scalars(self):
            class MockItems:
                def all(self):
                    return [card1, card2]
            return MockItems()
            
    mock_db.execute.return_value = MockResult()

    counts = {card1.id: 0, card2.id: 0}
    # Draw 1 card 1000 times
    for _ in range(1000):
        selected = await select_practice_cards(user_id, mock_db, count=1)
        assert len(selected) == 1
        counts[selected[0].id] += 1

    # card1 should be drawn roughly 90% of the time, card2 10% of the time.
    # give some margin: card1 between 800 and 1000 times
    assert 800 <= counts[card1.id] <= 1000
    assert 0 <= counts[card2.id] <= 200


def test_update_weight_after_review():
    # Grade GREEN
    card = Card(id=uuid.uuid4(), weight=1.0)
    update_weight_after_review(card, Grade.GREEN, False)
    assert round(card.weight, 2) == 0.7

    # Grade GREEN_STAR
    card = Card(id=uuid.uuid4(), weight=1.0)
    update_weight_after_review(card, Grade.GREEN_STAR, False)
    assert round(card.weight, 2) == 0.5

    # Grade YELLOW
    card = Card(id=uuid.uuid4(), weight=1.0)
    update_weight_after_review(card, Grade.YELLOW, False)
    assert round(card.weight, 2) == 1.2

    # Grade RED
    card = Card(id=uuid.uuid4(), weight=1.0)
    update_weight_after_review(card, Grade.RED, False)
    assert round(card.weight, 2) == 1.5

def test_update_weight_clamps_to_0_01():
    card = Card(id=uuid.uuid4(), weight=0.01)
    update_weight_after_review(card, Grade.GREEN_STAR, False)
    assert card.weight == 0.01

def test_update_weight_revealed():
    card = Card(id=uuid.uuid4(), weight=1.0)
    update_weight_after_review(card, Grade.GREEN, True)
    # first revealed -> * 2.0 = 2.0
    # then GREEN -> * 0.7 = 1.4
    assert round(card.weight, 2) == 1.4

def test_update_weight_after_reveal():
    card = Card(id=uuid.uuid4(), weight=1.0)
    update_weight_after_reveal(card)
    assert card.weight == 2.0
