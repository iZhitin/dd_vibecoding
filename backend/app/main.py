import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, cards, practice, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title="DD API",
        version="0.1.0",
        lifespan=lifespan,
    )

    cors_origins = os.getenv("APP_URL", "http://localhost:5173")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[origins.strip() for origins in cors_origins.split(",")],
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
