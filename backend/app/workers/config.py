from arq.connections import RedisSettings
from arq.cron import cron

from app.core.config import get_settings
from app.workers.digest import send_daily_digests
from app.workers.llm_review import review_sentences
from app.workers.scheduler import smart_nudge_check

settings = get_settings()


class WorkerSettings:
    functions = [review_sentences, smart_nudge_check, send_daily_digests]
    cron_jobs = [
        cron(smart_nudge_check, minute=0),
        cron(send_daily_digests, minute=0)
    ]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
