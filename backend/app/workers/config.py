from arq.connections import RedisSettings

from app.core.config import get_settings
from app.workers.llm_review import review_sentences

settings = get_settings()


class WorkerSettings:
    functions = [review_sentences]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
