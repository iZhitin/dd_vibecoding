import logging
import re
import sys

import structlog

from app.core.config import get_settings

SENSITIVE_KEYS = {"password", "token", "secret", "authorization", "api_key", "email"}
EMAIL_REGEX = re.compile(r"([a-zA-Z0-9_.+-]+)@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+?")

def mask_email(email: str) -> str:
    if not isinstance(email, str):
        return "***"
    parts = email.split("@")
    if len(parts) == 2:
        username, domain = parts
        masked_username = f"{username[0]}***" if len(username) > 1 else "***"
        return f"{masked_username}@{domain}"
    return "***"

def scrub_sensitive_data(logger, method_name, event_dict):
    """
    Redact sensitive keys from log payload and mask emails in strings.
    """
    for key, value in list(event_dict.items()):
        key_lower = str(key).lower()
        
        if any(sensitive in key_lower for sensitive in SENSITIVE_KEYS):
            if "email" in key_lower and isinstance(value, str) and "@" in value:
                event_dict[key] = mask_email(value)
            else:
                event_dict[key] = "***REDACTED***"
            continue
            
        if isinstance(value, str):
            def replace_email(match):
                return mask_email(match.group(0))
            event_dict[key] = EMAIL_REGEX.sub(replace_email, value)
            
    return event_dict

def setup_logging() -> None:
    settings = get_settings()
    log_level = logging.DEBUG if settings.APP_ENV == "development" else logging.INFO

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        scrub_sensitive_data,
    ]

    if settings.APP_ENV == "development":
        processor = structlog.dev.ConsoleRenderer(colors=True)
    else:
        processor = structlog.processors.JSONRenderer()

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            processor,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "arq"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.addHandler(handler)
        logger.propagate = False

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
