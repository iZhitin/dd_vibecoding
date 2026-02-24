from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, cards, practice, users
from app.core.config import get_settings


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

    application.include_router(auth.router)
    application.include_router(cards.router)
    application.include_router(practice.router)
    application.include_router(users.router)

    @application.get("/health", tags=["system"])
    async def health_check():
        return {"status": "ok"}

    return application


app = create_app()
