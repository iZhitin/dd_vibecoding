# [INIT]-[002] Настроить backend: FastAPI + pyproject.toml + точка входа

**Статус:** Выполнена
**Дата:** 2026-02-24

## Что сделано

1. Создан `backend/pyproject.toml` с зависимостями проекта:
   - FastAPI >=0.115, Uvicorn >=0.34, SQLAlchemy[asyncio] >=2.0, asyncpg >=0.30, Alembic >=1.14
   - Pydantic >=2.10, pydantic-settings >=2.7, python-jose[cryptography] >=3.3
   - Arq >=0.26, httpx >=0.28, openai >=1.60, resend >=2.0
   - Dev-зависимости: pytest, pytest-asyncio, httpx, factory-boy, ruff
   - Build-система: setuptools >=75.0
2. Создан `backend/app/main.py` с FastAPI-приложением через app factory:
   - `create_app()` создаёт экземпляр `FastAPI(title="DD API", version="0.1.0")`
   - CORS middleware с origins из переменной окружения `APP_URL` (default: `http://localhost:5173`)
   - Health-check эндпоинт `GET /health` → `{"status": "ok"}`
   - Подключены роутеры с префиксами: `/api/auth`, `/api/cards`, `/api/practice`, `/api/me`
   - Lifespan context manager для будущих startup/shutdown событий
3. Создан пустой `backend/app/__init__.py`.
4. Созданы `__init__.py` во всех вложенных пакетах: `api/`, `api/routes/`, `models/`, `schemas/`, `services/`, `workers/`, `core/`.
5. Созданы роутеры-заглушки: `auth.py`, `cards.py`, `practice.py`, `users.py` в `app/api/routes/`.

## Критерии готовности (DoD)

- [x] `cd backend && pip install -e .` завершается без ошибок
- [x] `uvicorn app.main:app --reload` запускает сервер
- [x] `GET /health` возвращает `{"status": "ok"}`
- [x] `GET /docs` показывает Swagger UI

## ADR

Нет принятых архитектурных решений — задача инфраструктурная. Используется стандартный app factory паттерн FastAPI.
