import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.card import Card
from app.models.practice_log import Grade, PracticeLog
from app.models.practice_session import PracticeSession
from app.schemas.llm import SentenceReview, SessionReviewResponse
from app.workers.llm_review import review_sentences


@pytest.fixture
def mock_db():
    db = AsyncMock()
    
    # Store the log so we can inspect it later
    card = Card(id=uuid.uuid4(), word="test", translation="тест", weight=1.0)
    log = PracticeLog(
        id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        card_id=card.id,
        user_sentence="Test sentence",
        grade=None,
        llm_feedback=None,
        revealed_translation=False
    )
    log.card = card
    db._mock_log = log
    
    async def mock_get(model, id):
        if model == PracticeSession:
            return PracticeSession(id=id, user_id=uuid.uuid4())
        return None
        
    db.get.side_effect = mock_get
    
    async def mock_execute(stmt):
        class MockScalars:
            def all(self):
                return [db._mock_log]
        class MockResult:
            def scalars(self):
                return MockScalars()
        return MockResult()
        
    db.execute.side_effect = mock_execute
    db.commit = AsyncMock()
    return db


@pytest.fixture
def mock_db_context(mock_db):
    class AsyncContext:
        async def __aenter__(self):
            return mock_db
        async def __aexit__(self, exc_type, exc, tb):
            pass
    with patch("app.workers.llm_review.async_session_maker", return_value=AsyncContext()):
        yield mock_db


@pytest.fixture
def mock_httpx():
    with patch("app.workers.llm_review.httpx.AsyncClient") as mock:
        client_instance = mock.return_value.__aenter__.return_value
        post_mock = AsyncMock()
        client_instance.post = post_mock
        yield post_mock


@pytest.fixture
def mock_settings():
    with patch("app.workers.llm_review.get_settings") as mock:
        settings = MagicMock()
        settings.OPENROUTER_API_KEY = "test-sk"
        mock.return_value = settings
        yield settings


@pytest.fixture
def mock_srs():
    with patch("app.workers.llm_review.update_weight_after_review") as mock:
        yield mock


@pytest.mark.asyncio
async def test_review_valid_response(mock_db_context, mock_httpx, mock_settings, mock_srs):
    session_id = uuid.uuid4()
    
    review_response = SessionReviewResponse(
        reviews=[
            SentenceReview(
                grade=Grade.GREEN,
                corrected_sentence=None,
                explanation="Good",
                praise=None
            )
        ]
    )
    resp_mock = MagicMock()
    resp_mock.json.return_value = {
        "choices": [{"message": {"content": review_response.model_dump_json()}}]
    }
    mock_httpx.return_value = resp_mock
    
    ctx = {}
    await review_sentences(ctx, session_id)
    
    log = mock_db_context._mock_log
    
    assert log.grade == Grade.GREEN
    assert log.llm_feedback is not None
    assert log.llm_feedback["grade"] == Grade.GREEN.value
    
    mock_db_context.commit.assert_called_once()
    mock_srs.assert_called_once_with(log.card, Grade.GREEN, False)


@pytest.mark.asyncio
async def test_review_malformed_json(mock_db_context, mock_httpx, mock_settings, mock_srs, caplog):
    # If JSON is malformed, OpenAI client throws an Exception (e.g. ValidationError)
    # The worker catches it and retries 3 times, then returns.
    session_id = uuid.uuid4()
    
    mock_httpx.side_effect = Exception("Malformed JSON error")
    
    ctx = {}
    await review_sentences(ctx, session_id)
    
    log = mock_db_context._mock_log
    
    # Assert grade was NOT set
    assert log.grade is None
    assert log.llm_feedback is None
    
    # Verify commit wasn't called because we aborted
    mock_db_context.commit.assert_not_called()
    mock_srs.assert_not_called()
    assert "Max retries reached. Gracefully giving up." in caplog.text


@pytest.mark.asyncio
async def test_review_api_timeout(mock_db_context, mock_httpx, mock_settings, mock_srs, caplog):
    session_id = uuid.uuid4()
    
    mock_httpx.side_effect = TimeoutError("Timeout")
    
    # Let's speed up the sleep to not delay tests
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        ctx = {}
        await review_sentences(ctx, session_id)
        
        # We expect 2 sleeps: after failure 1 and failure 2. The 3rd failure just bails.
        assert mock_sleep.call_count == 2
        
    log = mock_db_context._mock_log
    assert log.grade is None
    
    assert "Max retries reached. Gracefully giving up." in caplog.text


@pytest.mark.asyncio
async def test_review_updates_weight(mock_db_context, mock_httpx, mock_settings):
    # This time we DO NOT mock srs so it actually updates the weight
    session_id = uuid.uuid4()
    
    review_response = SessionReviewResponse(
        reviews=[
            SentenceReview(
                grade=Grade.RED,
                corrected_sentence="This is correct",
                explanation="Wrong grammar",
                praise=None
            )
        ]
    )
    resp_mock = MagicMock()
    resp_mock.json.return_value = {
        "choices": [{"message": {"content": review_response.model_dump_json()}}]
    }
    mock_httpx.return_value = resp_mock
    
    # Original weight is 1.0 (from mock_db setup)
    assert mock_db_context._mock_log.card.weight == 1.0
    
    ctx = {}
    await review_sentences(ctx, session_id)
    
    log = mock_db_context._mock_log
    # With Grade.RED, weight should be updated to 1.5
    assert log.grade == Grade.RED
    assert log.card.weight == 1.5
