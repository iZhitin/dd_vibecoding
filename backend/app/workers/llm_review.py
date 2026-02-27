import asyncio
import logging
import uuid
from typing import Any

import httpx
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
    if not settings.OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY is missing. Skipping LLM review.")
        return

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
            "- RED: Grammatical error or incorrect word usage.\n\n"
            "Respond ONLY with a valid JSON object exactly matching this schema:\n"
            f"{SessionReviewResponse.model_json_schema()}\n\n"
            "Do not wrap the JSON in markdown code blocks."
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
                payload = {
                    "model": settings.LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    "temperature": 0.1,
                }
                headers = {
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                }

                async with httpx.AsyncClient(timeout=30.0) as http_client:
                    resp = await http_client.post(
                        settings.OPENROUTER_URL, json=payload, headers=headers
                    )
                    resp.raise_for_status()
                    data = resp.json()

                raw = data["choices"][0]["message"]["content"]
                cleaned = (
                    raw.strip()
                    .removeprefix("```json")
                    .removeprefix("```")
                    .removesuffix("```")
                    .strip()
                )
                parsed_response = SessionReviewResponse.model_validate_json(cleaned)
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
