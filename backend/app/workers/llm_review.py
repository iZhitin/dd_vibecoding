import asyncio
import logging
import uuid
from typing import Any

from openai import AsyncOpenAI
from openai.types.chat import ParsedChatCompletion
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.database import async_session_maker
from app.models.practice_log import PracticeLog
from app.models.practice_session import PracticeSession
from app.schemas.llm import SessionReviewResponse
from app.services.srs import update_weight_after_review

logger = logging.getLogger(__name__)


async def review_sentences(ctx: dict[str, Any], session_id: uuid.UUID) -> None:
    settings = get_settings()
    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY is missing. Skipping LLM review.")
        return

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async with async_session_maker() as db:
        session_obj = await db.get(PracticeSession, session_id)
        if not session_obj:
            logger.error(f"PracticeSession {session_id} not found")
            return

        stmt = (
            select(PracticeLog)
            .where(PracticeLog.session_id == session_id)
            .options(selectinload(PracticeLog.card))
        )
        result = await db.execute(stmt)
        logs = list(result.scalars().all())

        if not logs:
            logger.warning(f"No logs found for session {session_id}")
            return

        system_prompt = (
            "You are a language teacher reviewing student sentences.\n"
            "For each sentence, evaluate the usage of the target word.\n\n"
            "Grading criteria:\n"
            "- GREEN: Correct usage, no errors.\n"
            "- GREEN_STAR: Outstanding, creative, or advanced usage.\n"
            "- YELLOW: Minor issues (style, typo) but meaning is correct.\n"
            "- RED: Grammatical error or incorrect word usage."
        )

        user_content = ""
        for i, log in enumerate(logs):
            word = log.card.word
            translation = log.card.translation
            user_sentence = log.user_sentence
            user_content += (
                f"Sentence {i + 1}:\n"
                f"Target word: \"{word}\"\n"
                f"Translation: \"{translation}\"\n"
                f"Student's sentence: \"{user_sentence}\"\n\n"
            )

        max_retries = 3
        backoff = 1

        parsed_response = None
        for attempt in range(max_retries):
            try:
                completion: ParsedChatCompletion[
                    SessionReviewResponse
                ] = await client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    response_format=SessionReviewResponse,
                    timeout=30.0,
                )
                parsed_response = completion.choices[0].message.parsed
                break
            except Exception as e:
                logger.error(f"Error during OpenAI API call attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error("Max retries reached. Gracefully giving up.")
                    return
                await asyncio.sleep(backoff)
                backoff *= 2

        if not parsed_response:
            return

        if len(parsed_response.reviews) != len(logs):
            logger.error(
                f"LLM returned {len(parsed_response.reviews)} reviews, expected {len(logs)}"
            )
            return

        for log, review in zip(logs, parsed_response.reviews, strict=True):
            log.grade = review.grade
            log.llm_feedback = review.model_dump(mode="json")
            update_weight_after_review(log.card, log.grade, log.revealed_translation)

        try:
            await db.commit()
            logger.info(f"Successfully reviewed {len(logs)} sentences for session {session_id}")
        except Exception as e:
            logger.error(f"Failed to commit review results: {e}")
            await db.rollback()
            raise
