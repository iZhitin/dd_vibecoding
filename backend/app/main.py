import uuid
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import auth, cards, practice, translate, users
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.rate_limit import limiter

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title="DD API",
        version="0.1.0",
        lifespan=lifespan,
    )

    settings = get_settings()
    cors_origins = settings.APP_URL
    allow_origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
    if not allow_origins:
        allow_origins = ["http://localhost:5173"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    @application.middleware("http")
    async def logging_middleware(request: Request, call_next):
        request_id = str(uuid.uuid4())
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
        )
        response = await call_next(request)
        return response

    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    application.include_router(auth.router)
    application.include_router(cards.router)
    application.include_router(practice.router)
    application.include_router(translate.router)
    application.include_router(users.router)

    @application.get("/health", tags=["system"])
    async def health_check():
        return {"status": "ok"}

    return application


app = create_app()
