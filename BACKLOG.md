# BACKLOG.md — Project DD (Daily Dict)

**Версия:** 1.0
**Дата:** Февраль 2026
**Источники:** PRD.md (приоритет), TECHSPEC.md (технические детали)

> Каждая задача — самодостаточный промпт для coding-агента.
> Формат: Контекст → Действие → Критерии готовности (DoD).
> Порядок задач оптимизирован для последовательного выполнения.

---

## Технический стек (справочно)

- **Frontend:** React 18, Vite, Tailwind CSS (монохром), Zustand, Framer Motion
- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2
- **БД:** PostgreSQL 16+, Alembic (миграции)
- **Очередь:** Redis + Arq
- **AI:** OpenAI API (gpt-4o-mini — валидация, gpt-4o — digest)
- **Email:** Resend + React Email
- **Инфра:** Docker Compose, Nginx, GitHub Actions

## Структура проекта (эталон)

```
dd/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app factory
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py              # Dependency injection (get_db, get_current_user)
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── cards.py
│   │   │       ├── practice.py
│   │   │       └── users.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # SQLAlchemy declarative base
│   │   │   ├── user.py
│   │   │   ├── card.py
│   │   │   ├── practice_session.py
│   │   │   └── practice_log.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── card.py
│   │   │   ├── practice.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── card.py
│   │   │   ├── practice.py
│   │   │   ├── srs.py
│   │   │   ├── streak.py
│   │   │   └── translation.py
│   │   ├── workers/
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # Arq worker settings
│   │   │   ├── llm_review.py
│   │   │   ├── email_sender.py
│   │   │   └── scheduler.py
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── config.py            # pydantic-settings
│   │       ├── database.py          # async engine, session factory
│   │       └── security.py          # JWT encode/decode
│   ├── migrations/
│   │   ├── env.py
│   │   └── versions/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── factories.py
│   │   ├── test_auth.py
│   │   ├── test_cards.py
│   │   ├── test_practice.py
│   │   ├── test_srs.py
│   │   ├── test_streak.py
│   │   └── test_llm_review.py
│   ├── pyproject.toml
│   ├── alembic.ini
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── CapturePage.tsx
│   │   │   ├── PracticePage.tsx
│   │   │   ├── HistoryPage.tsx
│   │   │   └── ReviewPage.tsx
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── PracticeCard.tsx
│   │   │   ├── StreakBadge.tsx
│   │   │   └── TrafficLight.tsx
│   │   ├── stores/
│   │   │   ├── authStore.ts
│   │   │   ├── captureStore.ts
│   │   │   └── practiceStore.ts
│   │   ├── api/
│   │   │   ├── client.ts             # axios/fetch instance
│   │   │   ├── auth.ts
│   │   │   ├── cards.ts
│   │   │   └── practice.ts
│   │   └── lib/
│   │       └── utils.ts
│   ├── public/
│   │   └── manifest.json
│   ├── index.html
│   ├── tailwind.config.ts
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── nginx/
│   └── nginx.conf
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
├── PRD.md
├── TECHSPEC.md
└── BACKLOG.md
```

---

## Этап 1: INIT — Инициализация проекта

---

- [x] [INIT]-[001] Создать корневую структуру проекта и Git-репозиторий

  **Контекст:** Проект DD (Daily Dict) — PWA для изучения иностранного языка. Начинаем с нуля. Структура проекта описана в начале этого файла (секция «Структура проекта»).

  **Действие:**
  - Инициализировать Git-репозиторий в корне `dd/`.
  - Создать `.gitignore` для Python + Node.js + Docker (включить: `__pycache__`, `node_modules`, `.env`, `dist/`, `.venv`, `*.pyc`, `.pytest_cache`).
  - Создать файл `.env.example` со всеми переменными окружения (пустые значения):
    ```
    # Database
    DATABASE_URL=postgresql+asyncpg://dd:dd@localhost:5432/dd
    # Redis
    REDIS_URL=redis://localhost:6379/0
    # JWT
    JWT_SECRET_KEY=change-me
    JWT_ALGORITHM=HS256
    JWT_EXPIRE_MINUTES=10080
    # OpenAI
    OPENAI_API_KEY=
    # Translation API
    DEEPL_API_KEY=
    # Email (Resend)
    RESEND_API_KEY=
    RESEND_FROM_EMAIL=dd@yourdomain.com
    # App
    APP_URL=http://localhost:5173
    APP_ENV=development
    ```
  - Создать пустые директории (с `.gitkeep` внутри): `backend/app/api/routes/`, `backend/app/models/`, `backend/app/schemas/`, `backend/app/services/`, `backend/app/workers/`, `backend/app/core/`, `backend/migrations/versions/`, `backend/tests/`, `frontend/src/pages/`, `frontend/src/components/`, `frontend/src/stores/`, `frontend/src/api/`, `frontend/src/lib/`, `frontend/public/`, `nginx/`, `.github/workflows/`.

  **Критерии готовности (DoD):**
  - [ ] Git-репозиторий инициализирован, `.gitignore` корректно игнорирует лишние файлы
  - [ ] `.env.example` содержит все перечисленные переменные
  - [ ] Все директории из эталонной структуры существуют

---

- [x] [INIT]-[002] Настроить backend: FastAPI + pyproject.toml + точка входа

  **Контекст:** Структура проекта создана в [INIT]-[001]. Backend использует Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2.

  **Действие:**
  - Создать `backend/pyproject.toml` с зависимостями:
    ```toml
    [project]
    name = "dd-backend"
    version = "0.1.0"
    requires-python = ">=3.12"
    dependencies = [
        "fastapi>=0.115",
        "uvicorn[standard]>=0.34",
        "sqlalchemy[asyncio]>=2.0",
        "asyncpg>=0.30",
        "alembic>=1.14",
        "pydantic>=2.10",
        "pydantic-settings>=2.7",
        "python-jose[cryptography]>=3.3",
        "arq>=0.26",
        "httpx>=0.28",
        "openai>=1.60",
        "resend>=2.0",
    ]

    [project.optional-dependencies]
    dev = [
        "pytest>=8.0",
        "pytest-asyncio>=0.25",
        "httpx>=0.28",
        "factory-boy>=3.3",
        "ruff>=0.9",
    ]
    ```
  - Создать `backend/app/__init__.py` (пустой).
  - Создать `backend/app/main.py` с FastAPI-приложением:
    - Создать `app = FastAPI(title="DD API", version="0.1.0")`.
    - Добавить CORS middleware (origins из settings).
    - Добавить health-check эндпоинт `GET /health` → `{"status": "ok"}`.
    - Подключить роутеры (пока пустые заглушки) с префиксами: `/api/auth`, `/api/cards`, `/api/practice`, `/api/me`.
  - Создать пустые `__init__.py` во всех пакетах (`api/`, `api/routes/`, `models/`, `schemas/`, `services/`, `workers/`, `core/`).

  **Критерии готовности (DoD):**
  - [ ] `cd backend && pip install -e .` завершается без ошибок
  - [ ] `uvicorn app.main:app --reload` запускает сервер
  - [ ] `GET /health` возвращает `{"status": "ok"}`
  - [ ] `GET /docs` показывает Swagger UI

---

- [x] [INIT]-[003] Настроить конфигурацию через pydantic-settings

  **Контекст:** FastAPI-приложение создано в [INIT]-[002]. Переменные окружения описаны в `.env.example` ([INIT]-[001]).

  **Действие:**
  - Создать `backend/app/core/config.py`:
    - Класс `Settings(BaseSettings)` с полями: `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM` (default "HS256"), `JWT_EXPIRE_MINUTES` (default 10080 = 7 дней), `OPENAI_API_KEY`, `DEEPL_API_KEY`, `RESEND_API_KEY`, `RESEND_FROM_EMAIL`, `APP_URL`, `APP_ENV` (default "development").
    - `model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")`.
    - Singleton-функция `get_settings()` с `@lru_cache`.
  - Использовать `get_settings()` в `main.py` для CORS origins.

  **Критерии готовности (DoD):**
  - [ ] Создание `.env` с минимальными значениями и запуск `uvicorn` не падает
  - [ ] `get_settings()` возвращает объект `Settings` с корректными значениями из `.env`

---

- [x] [INIT]-[004] Настроить frontend: React + Vite + Tailwind + Zustand

  **Контекст:** Корневая структура проекта создана ([INIT]-[001]). Frontend — PWA на React 18 с Vite, Tailwind CSS (строгая монохромная типографика), Zustand (стейт), Framer Motion (анимации).

  **Действие:**
  - Инициализировать Vite-проект в `frontend/`: `npm create vite@latest . -- --template react-ts`.
  - Установить зависимости:
    ```bash
    npm install zustand framer-motion react-router-dom
    npm install -D tailwindcss @tailwindcss/vite
    ```
  - Настроить Tailwind CSS в `frontend/src/index.css`:
    ```css
    @import "tailwindcss";
    ```
  - Настроить `frontend/vite.config.ts` с плагином Tailwind:
    ```ts
    import { defineConfig } from "vite";
    import react from "@vitejs/plugin-react";
    import tailwindcss from "@tailwindcss/vite";
    export default defineConfig({
      plugins: [react(), tailwindcss()],
      server: { proxy: { "/api": "http://localhost:8000" } },
    });
    ```
  - Создать `frontend/src/App.tsx` с базовым React Router (BrowserRouter) и маршрутами-заглушками: `/` (redirect на `/capture`), `/login`, `/capture`, `/practice`, `/history`, `/review`.
  - Создать `frontend/src/main.tsx` — точка входа, рендерит `<App />`.
  - Применить монохромную палитру: убедиться, что в базовых стилях используется `font-sans`, тёмный текст на белом фоне, минимализм.

  **Критерии готовности (DoD):**
  - [ ] `cd frontend && npm run dev` запускает dev-сервер
  - [ ] Открытие `http://localhost:5173` показывает приложение без ошибок в консоли
  - [ ] Tailwind-классы работают (например, `text-gray-900` применяет цвет)
  - [ ] Навигация между маршрутами работает (заглушки)

---

- [x] [INIT]-[005] Настроить Docker Compose для dev-окружения

  **Контекст:** Backend ([INIT]-[002]) и Frontend ([INIT]-[004]) настроены. Нужны PostgreSQL и Redis для локальной разработки. Продакшн-инфра: Docker Compose + Nginx (TECHSPEC §9).

  **Действие:**
  - Создать `backend/Dockerfile`:
    ```dockerfile
    FROM python:3.12-slim
    WORKDIR /app
    COPY pyproject.toml .
    RUN pip install --no-cache-dir .
    COPY . .
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```
  - Создать `frontend/Dockerfile`:
    ```dockerfile
    FROM node:22-alpine AS build
    WORKDIR /app
    COPY package*.json .
    RUN npm ci
    COPY . .
    RUN npm run build

    FROM nginx:alpine
    COPY --from=build /app/dist /usr/share/nginx/html
    ```
  - Создать `docker-compose.dev.yml` с сервисами:
    - `db`: postgres:16-alpine, порт 5432, volume для данных, переменные `POSTGRES_USER=dd`, `POSTGRES_PASSWORD=dd`, `POSTGRES_DB=dd`.
    - `redis`: redis:7-alpine, порт 6379.
  - Создать `docker-compose.yml` (полный продакшн-стек, пока как шаблон):
    - `db`, `redis`, `backend`, `frontend`, `nginx`, `worker`.
  - Создать `nginx/nginx.conf` с базовой конфигурацией reverse proxy: `/api` → backend:8000, всё остальное → frontend static files.

  **Критерии готовности (DoD):**
  - [ ] `docker compose -f docker-compose.dev.yml up -d` поднимает PostgreSQL и Redis
  - [ ] PostgreSQL доступен на `localhost:5432`, Redis — на `localhost:6379`
  - [ ] Dockerfiles для backend и frontend собираются без ошибок (`docker build`)

---

- [x] [INIT]-[006] Настроить линтеры и форматтеры

  **Контекст:** Backend ([INIT]-[002]) и Frontend ([INIT]-[004]) настроены. Backend использует ruff, frontend — eslint + prettier.

  **Действие:**
  - **Backend:** Добавить секцию `[tool.ruff]` в `backend/pyproject.toml`:
    ```toml
    [tool.ruff]
    target-version = "py312"
    line-length = 100

    [tool.ruff.lint]
    select = ["E", "F", "I", "N", "UP", "B", "SIM"]

    [tool.pytest.ini_options]
    asyncio_mode = "auto"
    ```
  - **Frontend:** Создать `.prettierrc` в `frontend/`:
    ```json
    { "semi": true, "singleQuote": false, "tabWidth": 2, "trailingComma": "all" }
    ```
  - Убедиться, что eslint уже настроен через Vite-шаблон (react-ts). Если нет — настроить.
  - Добавить npm-скрипты в `frontend/package.json`: `"lint": "eslint src/"`, `"format": "prettier --write src/"`.

  **Критерии готовности (DoD):**
  - [ ] `cd backend && ruff check app/` выполняется без ошибок
  - [ ] `cd frontend && npm run lint` выполняется
  - [ ] `cd frontend && npx prettier --check src/` не находит проблем с форматированием

---

- [x] [INIT]-[007] Настроить GitHub Actions CI pipeline

  **Контекст:** Backend и frontend настроены, линтеры на месте. CI/CD: GitHub Actions (TECHSPEC §9). Пайплайн: push to main → lint → test → build docker image.

  **Действие:**
  - Создать `.github/workflows/ci.yml`:
    ```yaml
    name: CI
    on:
      push:
        branches: [main]
      pull_request:
        branches: [main]
    jobs:
      backend:
        runs-on: ubuntu-latest
        services:
          postgres:
            image: postgres:16-alpine
            env:
              POSTGRES_USER: dd
              POSTGRES_PASSWORD: dd
              POSTGRES_DB: dd_test
            ports: ["5432:5432"]
            options: >-
              --health-cmd pg_isready
              --health-interval 10s
              --health-timeout 5s
              --health-retries 5
          redis:
            image: redis:7-alpine
            ports: ["6379:6379"]
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: "3.12"
          - run: pip install -e ".[dev]"
            working-directory: backend
          - run: ruff check app/
            working-directory: backend
          - run: pytest tests/ -v
            working-directory: backend
            env:
              DATABASE_URL: postgresql+asyncpg://dd:dd@localhost:5432/dd_test
              REDIS_URL: redis://localhost:6379/0
              JWT_SECRET_KEY: test-secret
      frontend:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-node@v4
            with:
              node-version: "22"
          - run: npm ci
            working-directory: frontend
          - run: npm run lint
            working-directory: frontend
          - run: npm run build
            working-directory: frontend
    ```

  **Критерии готовности (DoD):**
  - [ ] Файл `.github/workflows/ci.yml` создан и синтаксически валиден
  - [ ] При пуше в main (или PR) запускаются jobs `backend` и `frontend`

---

- [x] [INIT]-[099] Уборка этапа INIT

  **Контекст:** Завершены задачи [INIT]-[001]–[INIT]-[007]. Проект инициализирован: backend (FastAPI), frontend (React+Vite), Docker, CI.

  **Действие:**
  - Удалить все `.gitkeep` из директорий, в которых уже есть файлы.
  - Удалить шаблонные файлы Vite, которые не нужны (например, `App.css`, `assets/react.svg`, дефолтный counter в `App.tsx`, если он остался).
  - Проверить, что нет дублирования конфигурации (например, CORS origins не захардкожены в двух местах).
  - Убедиться, что все секреты вынесены в `.env` и нигде нет реальных значений в коде.
  - Запустить `ruff check` на backend и `npm run lint` на frontend, исправить все предупреждения.

  **Критерии готовности (DoD):**
  - [x] Нет шаблонных файлов Vite (react.svg, дефолтные стили)
  - [x] Нет захардкоженных секретов в коде (grep на «sk-», «password», «secret» не находит ничего кроме `.env.example`)
  - [x] `ruff check` и `npm run lint` проходят без предупреждений

---

## Этап 2: DATA — Модель данных

---

- [x] [DATA]-[001] Настроить SQLAlchemy async engine и фабрику сессий

  **Контекст:** Backend настроен ([INIT]-[002]), конфигурация через pydantic-settings ([INIT]-[003]). `DATABASE_URL` доступен через `get_settings().DATABASE_URL`. PostgreSQL запускается через docker-compose.dev.yml.

  **Действие:**
  - Создать `backend/app/core/database.py`:
    - `create_async_engine` из SQLAlchemy с `DATABASE_URL` из settings.
    - `async_sessionmaker` для создания `AsyncSession`.
    - Async generator `get_db()` для dependency injection в FastAPI (yield session, с commit/rollback).
  - Создать `backend/app/models/base.py`:
    - `DeclarativeBase` — базовый класс для всех моделей.
    - Миксин `TimestampMixin` с полями `created_at` (server_default=now) и `updated_at` (onupdate=now).
    - Все первичные ключи — UUID (используя `uuid7` или `uuid4` с `mapped_column(default=uuid.uuid4)`).

  **Критерии готовности (DoD):**
  - [x] `from app.core.database import get_db` импортируется без ошибок
  - [x] `from app.models.base import Base, TimestampMixin` импортируется без ошибок
  - [x] `get_db()` — async generator, совместимый с `Depends()` в FastAPI

---

- [x] [DATA]-[002] Создать SQLAlchemy-модели: User, Card, PracticeSession, PracticeLog

  **Контекст:** База и миксины созданы ([DATA]-[001]). Модель данных основана на PRD §6 (приоритет) и TECHSPEC §4 (детали). Ключевые решения:
  - Таблица `users`: `id` (UUID PK), `email` (unique), `timezone`, `avg_practice_time` (Time, nullable), `streak_current` (int, default 0), `streak_frozen_count` (int, default 0), `last_practice_at` (timestamp, nullable), `is_frozen` (bool, default false).
  - Таблица `cards`: `id` (UUID PK), `user_id` (FK → users), `word` (text), `translation` (text), `context_sentence` (text, nullable), `weight` (float, default 1.0 — вес для SRS Probabilistic Sampling), `next_review_at` (timestamp, nullable).
  - Таблица `practice_sessions`: `id` (UUID PK), `user_id` (FK → users), `started_at`, `completed_at` (nullable), `status` (enum: ACTIVE, COMPLETED).
  - Таблица `practice_logs`: `id` (UUID PK), `session_id` (FK → practice_sessions), `card_id` (FK → cards), `user_sentence` (text), `grade` (enum: GREEN, GREEN_STAR, YELLOW, RED — 4 уровня из PRD §3.C), `llm_feedback` (JSONB, nullable), `revealed_translation` (bool, default false).
  - Grade enum: GREEN = без ошибок, GREEN_STAR = выдающееся использование, YELLOW = мелкие недочёты, RED = грамматическая ошибка.

  **Действие:**
  - Создать `backend/app/models/user.py` с моделью `User`, наследующей `Base` и `TimestampMixin`.
  - Создать `backend/app/models/card.py` с моделью `Card`. Добавить relationship к `User` (back_populates).
  - Создать `backend/app/models/practice_session.py` с моделью `PracticeSession`. Enum `SessionStatus`.
  - Создать `backend/app/models/practice_log.py` с моделью `PracticeLog`. Enum `Grade` (GREEN, GREEN_STAR, YELLOW, RED). JSONB для `llm_feedback`.
  - В `backend/app/models/__init__.py` импортировать все модели для Alembic autodiscovery.

  **Критерии готовности (DoD):**
  - [x] Все 4 модели импортируются: `from app.models import User, Card, PracticeSession, PracticeLog`
  - [x] `Grade` enum содержит 4 значения: GREEN, GREEN_STAR, YELLOW, RED
  - [x] Foreign key связи определены корректно (user→cards, session→logs, card→logs)
  - [x] `Card.weight` имеет default=1.0 и тип float

---

- [x] [DATA]-[003] Инициализировать Alembic и создать первую миграцию

  **Контекст:** SQLAlchemy-модели созданы ([DATA]-[002]). Alembic используется для версионирования схемы (TECHSPEC §4). PostgreSQL доступен через `docker-compose.dev.yml`.

  **Действие:**
  - Выполнить `cd backend && alembic init migrations` (если структура ещё не создана).
  - Настроить `backend/alembic.ini`: `sqlalchemy.url` оставить пустым (будет из env).
  - Настроить `backend/migrations/env.py`:
    - Импортировать `Base` из `app.models.base` и все модели из `app.models`.
    - Установить `target_metadata = Base.metadata`.
    - Использовать `DATABASE_URL` из `app.core.config.get_settings()`.
    - Настроить async-миграции через `run_async_migrations()`.
  - Сгенерировать первую миграцию: `alembic revision --autogenerate -m "initial schema"`.
  - Применить: `alembic upgrade head`.

  **Критерии готовности (DoD):**
  - [x] Файл миграции создан в `backend/migrations/versions/`
  - [x] `alembic upgrade head` создаёт таблицы `users`, `cards`, `practice_sessions`, `practice_logs` в PostgreSQL
  - [x] `alembic downgrade base` откатывает все таблицы
  - [x] `alembic current` показывает текущую ревизию

---

- [x] [DATA]-[004] Создать Pydantic-схемы (request/response) для всех сущностей

  **Контекст:** SQLAlchemy-модели существуют ([DATA]-[002]). API-эндпоинты описаны в TECHSPEC §5.1. Pydantic v2 используется для валидации.

  **Действие:**
  - Создать `backend/app/schemas/auth.py`:
    - `LoginRequest(email: EmailStr)`
    - `VerifyRequest(token: str)`
    - `TokenResponse(access_token: str, token_type: str = "bearer")`
  - Создать `backend/app/schemas/card.py`:
    - `CardCreate(word: str, translation: str, context_sentence: str | None = None)`
    - `CardRead(id: UUID, word: str, translation: str, context_sentence: str | None, weight: float, next_review_at: datetime | None, created_at: datetime)` — `model_config = ConfigDict(from_attributes=True)`.
    - `CardList(items: list[CardRead], total: int)`
  - Создать `backend/app/schemas/practice.py`:
    - `PracticeCardRead(card_id: UUID, word: str, context_sentence: str | None, previous_sentence: str | None)` — данные карточки для практики (перевод НЕ включён — он скрыт под кнопкой, PRD §4.2).
    - `DailyPracticeResponse(session_id: UUID, cards: list[PracticeCardRead])`
    - `SentenceSubmit(card_id: UUID, user_sentence: str, revealed_translation: bool = False)`
    - `PracticeSubmitRequest(session_id: UUID, sentences: list[SentenceSubmit])` — ровно 10 записей.
    - Валидатор: `len(sentences) == 10`, иначе `ValidationError`.
  - Создать `backend/app/schemas/user.py`:
    - `UserRead(id: UUID, email: str, timezone: str | None, streak_current: int, streak_frozen_count: int, last_practice_at: datetime | None)`
    - `TimezoneUpdate(timezone: str)` — валидация: timezone должен быть валидным IANA timezone.

  **Критерии готовности (DoD):**
  - [x] Все схемы импортируются без ошибок
  - [x] `PracticeSubmitRequest` отклоняет payload с количеством sentences != 10
  - [x] `CardRead` корректно сериализует SQLAlchemy-модель (from_attributes=True)

---

- [x] [DATA]-[005] Создать seed-данные для разработки

  **Контекст:** Модели и миграции готовы ([DATA]-[002], [DATA]-[003]). Для разработки frontend и ручного тестирования нужны демо-данные.

  **Действие:**
  - Создать `backend/scripts/seed.py` (standalone-скрипт, запускаемый через `python -m scripts.seed`):
    - Создать 1 тестового пользователя: `email="test@dd.local"`, `timezone="Europe/Moscow"`, `streak_current=5`.
    - Создать 15 карточек (слов) с разными весами (от 0.1 до 2.0), разными `next_review_at` (часть — в прошлом, часть — в будущем).
    - Создать 2 завершённые `PracticeSession` с 10 `PracticeLog` каждая (разные грейды).
    - Использовать async session из `app.core.database`.
  - Добавить скрипт `seed` в pyproject.toml scripts или документировать запуск.

  **Критерии готовности (DoD):**
  - [x] `python -m scripts.seed` заполняет БД тестовыми данными без ошибок
  - [x] Повторный запуск не создаёт дубликатов (проверка по email)
  - [x] В БД есть пользователь, 15 карточек, 2 сессии, 20 логов

---

- [x] [DATA]-[099] Уборка этапа DATA

  **Контекст:** Завершены задачи [DATA]-[001]–[DATA]-[005]. Модель данных, миграции, схемы и seed-данные готовы.

  **Действие:**
  - Проверить, что все модели используют единообразные соглашения: snake_case для полей, PascalCase для классов.
  - Убедиться, что нет дублирования между Pydantic-схемами (общие базовые классы где уместно).
  - Проверить, что все enum-значения совпадают между моделями и схемами.
  - Убедиться, что `Base.metadata` содержит все 4 таблицы.
  - Запустить `ruff check app/models/ app/schemas/` — исправить все предупреждения.

  **Критерии готовности (DoD):**
  - [x] Единообразное именование во всех моделях и схемах
  - [x] Нет дублирования полей/определений
  - [x] `ruff check` проходит без предупреждений на models/ и schemas/

---

## Этап 3: AUTH — Аутентификация

---

- [x] [AUTH]-[001] Реализовать генерацию и отправку Magic Link

  **Контекст:** Модели и схемы существуют ([DATA]-[002], [DATA]-[004]). Auth: passwordless через Magic Link (PRD §5.2, TECHSPEC §5.1). Пользователь вводит email → получает письмо со ссылкой → кликает → попадает в приложение.

  **Действие:**
  - Создать `backend/app/core/security.py`:
    - Функция `create_magic_token(email: str) -> str`: генерирует JWT-токен с payload `{"email": email, "type": "magic", "exp": now + 15 min}`, подписанный `JWT_SECRET_KEY`.
    - Функция `verify_magic_token(token: str) -> str | None`: декодирует токен, проверяет `type == "magic"`, возвращает email или None при ошибке/истечении.
    - Функция `create_access_token(user_id: UUID) -> str`: JWT с payload `{"sub": str(user_id), "type": "access", "exp": now + JWT_EXPIRE_MINUTES}`.
    - Функция `verify_access_token(token: str) -> UUID | None`: декодирует, проверяет `type == "access"`, возвращает user_id.
  - Создать `backend/app/services/auth.py`:
    - `async def request_magic_link(email: str, db: AsyncSession)`:
      1. Найти или создать пользователя по email.
      2. Сгенерировать magic token.
      3. Сформировать URL: `{APP_URL}/auth/verify?token={token}`.
      4. Отправить email через Resend (пока заглушка — print URL в console, реальная отправка будет в [NOTIFY]).
      5. Вернуть `{"message": "Magic link sent"}`.
    - `async def verify_magic_link(token: str, db: AsyncSession)`:
      1. Верифицировать magic token → получить email.
      2. Найти пользователя по email (должен существовать после request).
      3. Создать access token с user_id.
      4. Вернуть `TokenResponse`.
  - Создать `backend/app/api/routes/auth.py`:
    - `POST /api/auth/login` — принимает `LoginRequest`, вызывает `request_magic_link`.
    - `POST /api/auth/verify` — принимает `VerifyRequest`, вызывает `verify_magic_link`, возвращает `TokenResponse`.

  **Критерии готовности (DoD):**
  - [x] `POST /api/auth/login` с `{"email": "test@example.com"}` возвращает 200 и логирует magic link в консоль
  - [x] `POST /api/auth/verify` с валидным токеном возвращает `{"access_token": "...", "token_type": "bearer"}`
  - [x] Просроченный magic token (>15 мин) возвращает 401
  - [x] Повторный `POST /api/auth/login` для нового email создаёт пользователя в БД

---

- [x] [AUTH]-[002] Реализовать middleware защиты роутов (get_current_user)

  **Контекст:** JWT-токены генерируются и верифицируются ([AUTH]-[001]). Нужен dependency injection для защиты эндпоинтов — `get_current_user`, который извлекает user из Bearer-токена.

  **Действие:**
  - Создать `backend/app/api/deps.py`:
    - `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)`.
    - `async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User`:
      1. Если токен отсутствует → `HTTPException(401, "Not authenticated")`.
      2. Верифицировать access token → получить `user_id`.
      3. Если невалидный/просрочен → `HTTPException(401, "Invalid token")`.
      4. Найти пользователя по `user_id` в БД.
      5. Если не найден → `HTTPException(401, "User not found")`.
      6. Вернуть объект `User`.
  - Подключить `get_current_user` как зависимость в роутах (пока не создавать новые роуты, только подготовить dependency).

  **Критерии готовности (DoD):**
  - [ ] `get_current_user` корректно извлекает пользователя из Bearer-токена
  - [ ] Запрос без токена возвращает 401
  - [ ] Запрос с невалидным токеном возвращает 401
  - [ ] Запрос с валидным токеном возвращает объект User

---

- [x] [AUTH]-[003] Реализовать эндпоинт GET /api/me и POST /api/me/timezone

  **Контекст:** Middleware `get_current_user` готов ([AUTH]-[002]). Схемы `UserRead` и `TimezoneUpdate` созданы ([DATA]-[004]). TECHSPEC §5.1: `GET /me` (Stats, Settings), `POST /me/timezone` (Update local time).

  **Действие:**
  - Создать `backend/app/api/routes/users.py`:
    - `GET /api/me` → зависимость `current_user = Depends(get_current_user)` → вернуть `UserRead` из модели.
    - `POST /api/me/timezone` → принимает `TimezoneUpdate`, обновляет `current_user.timezone` в БД, возвращает обновлённый `UserRead`.
  - Подключить роутер в `main.py`.

  **Критерии готовности (DoD):**
  - [ ] `GET /api/me` с валидным токеном возвращает данные пользователя
  - [ ] `POST /api/me/timezone` с `{"timezone": "Europe/Berlin"}` обновляет таймзону
  - [ ] Невалидная таймзона (например, `"Mars/Olympus"`) возвращает 422

---

- [x] [AUTH]-[099] Уборка этапа AUTH

  **Контекст:** Завершены задачи [AUTH]-[001]–[AUTH]-[003]. Auth-flow работает: magic link → verify → JWT → protected routes.

  **Действие:**
  - Проверить, что JWT-секрет не захардкожен нигде, кроме `.env`.
  - Убедиться, что magic token используется одноразово (опционально: добавить механизм инвалидации использованных magic-токенов, если не реализован).
  - Проверить, что все auth-роуты возвращают корректные HTTP-статусы (200, 201, 401, 422).
  - Удалить print-заглушки для magic link URL, если они были для дебага (заменить на logging).
  - Запустить `ruff check app/core/security.py app/services/auth.py app/api/routes/auth.py app/api/deps.py`.

  **Критерии готовности (DoD):**
  - [ ] Нет захардкоженных секретов
  - [ ] Все auth-ошибки возвращают JSON с описанием, а не стектрейс
  - [ ] `ruff check` проходит без предупреждений

---

## Этап 4: CORE — Ядро бизнес-логики

---

- [x] [CORE]-[001] Реализовать POST /api/cards — Capture (ввод нового слова)

  **Контекст:** Auth работает ([AUTH]-[002]), модели и схемы готовы ([DATA]-[002], [DATA]-[004]). Capture flow из PRD §3.A: пользователь вводит слово → система сохраняет карточку. Перевод на этом этапе приходит от пользователя (автоперевод будет в [CORE]-[002]).

  **Действие:**
  - Создать `backend/app/services/card.py`:
    - `async def create_card(user_id: UUID, data: CardCreate, db: AsyncSession) -> Card`:
      1. Создать объект `Card` с `user_id`, `word=data.word`, `translation=data.translation`, `context_sentence=data.context_sentence`, `weight=1.0`, `next_review_at=now`.
      2. Сохранить в БД.
      3. Вернуть созданный объект.
  - Создать `backend/app/api/routes/cards.py`:
    - `POST /api/cards` — protected (`Depends(get_current_user)`), принимает `CardCreate`, вызывает `create_card`, возвращает `CardRead` с кодом 201.
    - `GET /api/cards` — protected, возвращает `CardList` со всеми карточками пользователя, отсортированными по `created_at` desc. Поддержка пагинации: query params `offset` (default 0) и `limit` (default 50).
  - Подключить роутер в `main.py`.

  **Критерии готовности (DoD):**
  - [x] `POST /api/cards` с `{"word": "serendipity", "translation": "счастливая случайность"}` возвращает 201 и JSON карточки
  - [x] `GET /api/cards` возвращает список карточек текущего пользователя
  - [x] Карточки одного пользователя не видны другому
  - [x] Пагинация работает (offset/limit)

---

- [x] [CORE]-[002] Интегрировать Dictionary API для автоперевода

  **Контекст:** Capture endpoint работает ([CORE]-[001]). PRD §4.1: интеграция с Dictionary API (Google Translate / DeepL / OpenAI). TECHSPEC §6 Scenario A: Optimistic UI — UI показывает skeleton, пока грузится перевод. Fallback: если API недоступен, пользователь вводит перевод вручную (TECHSPEC §7).

  **Действие:**
  - Создать `backend/app/services/translation.py`:
    - `async def translate_word(word: str) -> str | None`:
      1. Попытаться перевести через DeepL API (если `DEEPL_API_KEY` задан), используя `httpx.AsyncClient`.
      2. Если DeepL недоступен или ключ не задан — попробовать OpenAI API (gpt-4o-mini): промпт «Translate the word "{word}" to Russian. Return only the translation, no explanations.»
      3. Если оба API недоступны — вернуть `None`.
      4. Timeout: 5 секунд на каждый запрос.
  - Создать новый эндпоинт `POST /api/translate` в `backend/app/api/routes/cards.py`:
    - Принимает `{"word": "serendipity"}`.
    - Вызывает `translate_word`.
    - Возвращает `{"word": "serendipity", "translation": "счастливая случайность"}` или `{"word": "serendipity", "translation": null}` если перевод не удался.
  - Этот эндпоинт protected (`Depends(get_current_user)`).

  **Критерии готовности (DoD):**
  - [x] `POST /api/translate` с `{"word": "hello"}` возвращает перевод (при наличии API ключа)
  - [x] При недоступности API возвращает `{"translation": null}` (не 500)
  - [x] Timeout не превышает 5 секунд

---

- [x] [CORE]-[003] Реализовать SRS-алгоритм (вероятностная выборка)

  **Контекст:** Карточки создаются ([CORE]-[001]). Алгоритм SRS из PRD §4.3 — **Probabilistic Sampling** (не жёсткие интервалы):

  **Бизнес-правила (PRD §4.3, дословно):**
  - Вероятностная выборка: каждое слово имеет `weight` (float, default 1.0).
  - Нажатие «Reveal Translation» → вес резко растёт (например, `weight *= 2.0`).
  - Ошибка в предложении (AI Review, grade=RED) → вес растёт (например, `weight *= 1.5`).
  - Мелкий недочёт (grade=YELLOW) → вес немного растёт (`weight *= 1.2`).
  - Успех (grade=GREEN) → вес снижается (`weight *= 0.7`), но не ниже 0.01.
  - Выдающееся использование (grade=GREEN_STAR) → вес снижается сильнее (`weight *= 0.5`), min 0.01.
  - Нет «архива» — слово навсегда остаётся в длинном хвосте (Infinite Tail).
  - Выборка 10 карточек: случайный выбор с вероятностью, пропорциональной `weight / sum(all_weights)`.

  **Действие:**
  - Создать `backend/app/services/srs.py`:
    - `async def select_practice_cards(user_id: UUID, db: AsyncSession, count: int = 10) -> list[Card]`:
      1. Получить все карточки пользователя с `weight > 0`.
      2. Если карточек меньше `count` — вернуть все.
      3. Рассчитать вероятности: `p_i = weight_i / sum(weights)`.
      4. Выбрать `count` карточек без повторений с помощью `random.choices` (weighted) или numpy-подобного подхода.
      5. Вернуть выбранные карточки.
    - `def update_weight_after_review(card: Card, grade: Grade, revealed: bool) -> None`:
      1. Если `revealed` → `card.weight *= 2.0`.
      2. Применить множитель по grade: RED → `*= 1.5`, YELLOW → `*= 1.2`, GREEN → `*= 0.7`, GREEN_STAR → `*= 0.5`.
      3. Clamp: `card.weight = max(card.weight, 0.01)`.
    - `def update_weight_after_reveal(card: Card) -> None`:
      1. `card.weight *= 2.0`.

  **Критерии готовности (DoD):**
  - [x] `select_practice_cards` возвращает 10 карточек (или меньше, если в базе мало)
  - [x] Карточки с большим весом выбираются чаще (статистическая проверка: при 1000 выборок)
  - [x] `update_weight_after_review` корректно обновляет вес для всех 4 грейдов
  - [x] Вес никогда не падает ниже 0.01

---

- [x] [CORE]-[004] Реализовать GET /api/practice/daily — генерация сессии

  **Контекст:** SRS-алгоритм реализован ([CORE]-[003]). PRD §4.2: строго 10 карточек. TECHSPEC §5.1: `GET /practice/daily` генерирует и возвращает 10 слов. Для каждой карточки нужно показать предыдущее предложение пользователя (Context Cue, PRD §3.B) — берётся из последнего `PracticeLog` для этой карточки.

  **Действие:**
  - Создать `backend/app/services/practice.py`:
    - `async def generate_daily_session(user_id: UUID, db: AsyncSession) -> tuple[PracticeSession, list[PracticeCardRead]]`:
      1. Проверить: нет ли уже активной сессии (status=ACTIVE) у пользователя. Если есть — вернуть её (не создавать новую).
      2. Вызвать `select_practice_cards(user_id, db, count=10)`.
      3. Для каждой карточки найти последний `PracticeLog` (если есть) — взять `user_sentence` как `previous_sentence`.
      4. Создать `PracticeSession(user_id, status=ACTIVE, started_at=now)`.
      5. Вернуть сессию и список `PracticeCardRead`.
  - Создать `backend/app/api/routes/practice.py`:
    - `GET /api/practice/daily` — protected, вызывает `generate_daily_session`, возвращает `DailyPracticeResponse`.
  - Подключить роутер в `main.py`.

  **Критерии готовности (DoD):**
  - [x] `GET /api/practice/daily` возвращает `session_id` + список из 10 карточек
  - [x] Каждая карточка содержит `card_id`, `word`, `context_sentence`, `previous_sentence` (nullable)
  - [x] Перевод НЕ включён в ответ (скрыт под кнопкой на UI)
  - [x] Повторный вызов при активной сессии возвращает ту же сессию

---

- [x] [CORE]-[005] Реализовать POST /api/practice/submit — отправка результатов сессии

  **Контекст:** Генерация сессии работает ([CORE]-[004]). TECHSPEC §6 Scenario B: пользователь заполняет 10 предложений → Submit → сервер сохраняет PracticeSession + PracticeLog → запускает LLM-review (асинхронно). PRD §4.2: soft-проверка на copy-paste предыдущего ответа.

  **Действие:**
  - Добавить в `backend/app/services/practice.py`:
    - `async def submit_practice(user_id: UUID, data: PracticeSubmitRequest, db: AsyncSession) -> PracticeSession`:
      1. Найти сессию по `data.session_id`, проверить что она принадлежит `user_id` и `status == ACTIVE`.
      2. Для каждого `SentenceSubmit` в `data.sentences`:
         a. Проверить, что `card_id` принадлежит пользователю.
         b. Soft-check: если `user_sentence` совпадает с предыдущим `PracticeLog.user_sentence` для этой карточки — пометить (пока просто логировать).
         c. Создать `PracticeLog(session_id, card_id, user_sentence, revealed_translation=revealed, grade=None, llm_feedback=None)`.
         d. Если `revealed_translation == True` — вызвать `update_weight_after_reveal(card)`.
      3. Обновить `PracticeSession.status = COMPLETED`, `completed_at = now`.
      4. Обновить `User.last_practice_at = now`.
      5. Поставить задачу в очередь на LLM-review (пока заглушка: `# TODO: enqueue llm_review task`).
      6. Вернуть обновлённую сессию.
  - Добавить в `backend/app/api/routes/practice.py`:
    - `POST /api/practice/submit` — protected, принимает `PracticeSubmitRequest`, вызывает `submit_practice`, возвращает 200.

  **Критерии готовности (DoD):**
  - [ ] `POST /api/practice/submit` с 10 предложениями возвращает 200
  - [ ] Сессия переходит в статус COMPLETED
  - [ ] 10 записей PracticeLog создаются в БД
  - [ ] `User.last_practice_at` обновляется
  - [ ] Попытка submit чужой сессии → 403
  - [ ] Попытка submit завершённой сессии → 400

---

- [x] [CORE]-[006] Реализовать GET /api/cards/:id/translation — получение перевода (Reveal)

  **Контекст:** Practice flow работает ([CORE]-[004], [CORE]-[005]). PRD §3.B: кнопка «Reveal Translation» скрыта, при нажатии показывает перевод. PRD §4.3: нажатие Reveal → вес слова резко растёт.

  **Действие:**
  - Добавить в `backend/app/api/routes/cards.py`:
    - `GET /api/cards/{card_id}/translation` — protected.
      1. Найти карточку по `card_id`, проверить что принадлежит текущему пользователю.
      2. Вернуть `{"card_id": card_id, "translation": card.translation}`.
  - Обновление веса будет отмечено в `PracticeSubmitRequest.revealed_translation` при отправке сессии ([CORE]-[005] уже обрабатывает это).

  **Критерии готовности (DoD):**
  - [x] `GET /api/cards/{card_id}/translation` возвращает перевод
  - [x] Чужая карточка → 404
  - [x] Без авторизации → 401

---

- [x] [CORE]-[007] Реализовать Streak-логику

  **Контекст:** Practice submit обновляет `User.last_practice_at` ([CORE]-[005]). Streak-правила из PRD §4.4:
  - **No Debt:** Пропущенные дни сгорают — стрик обнуляется.
  - `streak_current` увеличивается на 1 при каждой завершённой сессии, если предыдущая практика была вчера (или сегодня — первая практика за день).
  - Если `last_practice_at` был позавчера или раньше → `streak_current = 1` (начать заново).
  - `is_frozen = True` → стрик не сбрасывается один пропущенный день, `streak_frozen_count -= 1`, `is_frozen = False`.
  - Recovery: ручной процесс (MVP), не автоматизируется.

  **Действие:**
  - Создать `backend/app/services/streak.py`:
    - `async def update_streak(user: User, db: AsyncSession) -> User`:
      1. `today = date.today()` (в таймзоне пользователя, конвертировать из UTC).
      2. Если `last_practice_at` — сегодня → ничего не менять (уже практиковался).
      3. Если `last_practice_at` — вчера → `streak_current += 1`.
      4. Если `last_practice_at` — позавчера и `is_frozen and streak_frozen_count > 0` → `streak_frozen_count -= 1`, `is_frozen = False`, `streak_current += 1`.
      5. Иначе (пропуск > 1 дня без заморозки) → `streak_current = 1`.
      6. Если `last_practice_at is None` (первая практика) → `streak_current = 1`.
      7. Обновить `last_practice_at = now(UTC)`.
      8. Сохранить в БД.
  - Встроить вызов `update_streak(user, db)` в `submit_practice` ([CORE]-[005]) **перед** обновлением `last_practice_at`.

  **Критерии готовности (DoD):**
  - [x] Практика каждый день подряд → streak растёт (1, 2, 3, ...)
  - [x] Пропуск дня → streak = 1
  - [x] Заморозка: при `is_frozen=True, streak_frozen_count=1` пропуск не обнуляет streak
  - [x] Две практики в один день → streak не меняется (не +2)

---

- [x] [CORE]-[099] Уборка этапа CORE

  **Контекст:** Завершены задачи [CORE]-[001]–[CORE]-[007]. Backend API: cards CRUD, translation, practice session, SRS, streak.

  **Действие:**
  - Проверить единообразие HTTP-статусов: 200 для GET/PUT, 201 для POST (создание), 400/403/404/422 для ошибок.
  - Убедиться, что все SQL-запросы используют `select()` и не делают N+1 (особенно в `generate_daily_session`).
  - Проверить, что SRS-множители (2.0, 1.5, 1.2, 0.7, 0.5) вынесены в константы (конфиг или модуль `srs.py`), а не захардкожены в коде.
  - Удалить TODO-заглушки, которые были заменены реальным кодом.
  - Проверить, что `submit_practice` транзакционно: либо все 10 логов сохранены, либо ни одного.
  - Запустить `ruff check app/services/ app/api/routes/`.

  **Критерии готовности (DoD):**
  - [x] Нет N+1 запросов в API-эндпоинтах
  - [x] SRS-коэффициенты вынесены в именованные константы
  - [x] `submit_practice` атомарный (транзакция)
  - [x] `ruff check` проходит без предупреждений

---

## Этап 5: AI — Интеграция LLM

---

- [x] [AI]-[001] Настроить Arq worker и подключение к Redis

  **Контекст:** Redis запускается через docker-compose.dev.yml ([INIT]-[005]). `REDIS_URL` доступен через settings ([INIT]-[003]). Arq — легковесный task queue на Python (TECHSPEC §3).

  **Действие:**
  - Создать `backend/app/workers/config.py`:
    - Настроить `ArqRedis` connection pool.
    - Определить `WorkerSettings` класс для Arq:
      ```python
      class WorkerSettings:
          functions = [review_sentences]
          redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
      ```
  - Добавить команду запуска воркера: `arq app.workers.config.WorkerSettings`.
  - Добавить `worker` сервис в `docker-compose.yml`:
    ```yaml
    worker:
      build: ./backend
      command: arq app.workers.config.WorkerSettings
      depends_on: [db, redis]
    ```

  **Критерии готовности (DoD):**
  - [ ] `arq app.workers.config.WorkerSettings` запускает воркер без ошибок
  - [ ] Воркер подключается к Redis и ждёт задач
  - [ ] Воркер добавлен в docker-compose.yml

---

- [x] [AI]-[002] Создать Pydantic-схему для LLM-ответа (Traffic Light)

  **Контекст:** PRD §3.C описывает Traffic Light Report: GREEN (без ошибок), GREEN_STAR (выдающееся использование), YELLOW (мелкие недочёты), RED (грамматическая ошибка). TECHSPEC §5.2: строгий JSON-формат для ответа LLM (pydantic model).

  **Действие:**
  - Создать `backend/app/schemas/llm.py`:
    ```python
    class SentenceReview(BaseModel):
        grade: Grade  # GREEN, GREEN_STAR, YELLOW, RED
        corrected_sentence: str | None = None  # Исправленная версия (для YELLOW/RED)
        explanation: str  # Объяснение оценки
        praise: str | None = None  # Похвала (для GREEN_STAR)

    class SessionReviewResponse(BaseModel):
        reviews: list[SentenceReview]
    ```
  - Этот формат будет использован как `response_format` при вызове OpenAI (structured output).

  **Критерии готовности (DoD):**
  - [ ] `SentenceReview` валидирует JSON с полями grade, corrected_sentence, explanation, praise
  - [ ] `Grade` enum совпадает с определённым в моделях ([DATA]-[002])
  - [ ] `SessionReviewResponse` содержит список ровно из N ревью

---

- [x] [AI]-[003] Реализовать LLM Review Worker

  **Контекст:** Arq worker настроен ([AI]-[001]), схема ответа определена ([AI]-[002]). TECHSPEC §6 Scenario B: после submit воркер отправляет предложения на проверку LLM. PRD §5.2: gpt-4o-mini для валидации. TECHSPEC §7: Retry x3 с exp. backoff, при недоступности — сохранить raw logs.

  **Действие:**
  - Создать `backend/app/workers/llm_review.py`:
    - `async def review_sentences(ctx, session_id: UUID)`:
      1. Получить `PracticeSession` и все связанные `PracticeLog` из БД.
      2. Для каждого лога получить `Card.word` и `Card.translation`.
      3. Сформировать промпт для OpenAI:
         ```
         You are a language teacher reviewing student sentences.
         For each sentence, evaluate the usage of the target word.

         Target word: "{word}"
         Translation: "{translation}"
         Student's sentence: "{user_sentence}"

         Respond with a JSON object:
         {
           "grade": "GREEN" | "GREEN_STAR" | "YELLOW" | "RED",
           "corrected_sentence": null or "corrected version",
           "explanation": "brief explanation",
           "praise": null or "praise for outstanding usage"
         }

         Grading criteria:
         - GREEN: Correct usage, no errors.
         - GREEN_STAR: Outstanding, creative, or advanced usage.
         - YELLOW: Minor issues (style, typo) but meaning is correct.
         - RED: Grammatical error or incorrect word usage.
         ```
      4. Вызвать OpenAI API (model=gpt-4o-mini) с `response_format` для structured JSON output.
      5. Парсить ответ через `SessionReviewResponse`.
      6. Обновить каждый `PracticeLog`: `grade`, `llm_feedback` (полный JSON ответа).
      7. Вызвать `update_weight_after_review(card, grade, revealed)` из SRS ([CORE]-[003]) для каждой карточки.
      8. Retry-логика: 3 попытки с exponential backoff (1s, 2s, 4s). При полной неудаче — логировать ошибку, оставить `grade=None`.

  **Критерии готовности (DoD):**
  - [ ] Воркер получает задачу `review_sentences(session_id)` и обрабатывает её
  - [ ] `PracticeLog.grade` и `PracticeLog.llm_feedback` заполняются после обработки
  - [ ] `Card.weight` обновляется согласно SRS-правилам
  - [ ] При ошибке OpenAI API логи сохраняются без grade (graceful degradation)
  - [ ] Retry 3 раза с exp. backoff

---

- [x] [AI]-[004] Подключить enqueue LLM-review в submit_practice

  **Контекст:** LLM worker работает ([AI]-[003]). В `submit_practice` ([CORE]-[005]) есть TODO-заглушка для постановки задачи в очередь.

  **Действие:**
  - В `backend/app/services/practice.py`:
    - Импортировать `ArqRedis` и создать функцию `get_arq_pool()` для получения пула Redis.
    - В `submit_practice`, после сохранения логов, добавить:
      ```python
      pool = await get_arq_pool()
      await pool.enqueue_job("review_sentences", session.id)
      ```
  - Убрать TODO-комментарий.

  **Критерии готовности (DoD):**
  - [ ] `POST /api/practice/submit` ставит задачу `review_sentences` в очередь Redis
  - [ ] Воркер подхватывает задачу и обрабатывает (видно в логах воркера)
  - [ ] PracticeLog обновляется с grade и llm_feedback (проверить через БД или GET-эндпоинт)

---

- [x] [AI]-[099] Уборка этапа AI

  **Контекст:** Завершены задачи [AI]-[001]–[AI]-[004]. LLM-review работает асинхронно.

  **Действие:**
  - Проверить, что промпт для LLM не содержит injection-уязвимостей (пользовательский текст экранирован).
  - Убедиться, что OpenAI API ключ не логируется.
  - Проверить, что при `OPENAI_API_KEY=""` воркер не крашится, а gracefully пропускает review.
  - Проверить, что JSON-парсинг LLM-ответа обрабатывает malformed responses (TECHSPEC §10: Mock_LLM test).
  - Запустить `ruff check app/workers/ app/schemas/llm.py`.

  **Критерии готовности (DoD):**
  - [ ] Промпт экранирует пользовательский ввод
  - [ ] API-ключ не появляется в логах
  - [ ] Malformed LLM-ответ не крашит воркер
  - [ ] `ruff check` чисто

---

## Этап 6: NOTIFY — Система уведомлений

---

- [x] [NOTIFY]-[001] Интегрировать Resend для отправки email

  **Контекст:** Resend — email-провайдер из PRD §5.3. `RESEND_API_KEY` и `RESEND_FROM_EMAIL` доступны из settings ([INIT]-[003]).

  **Действие:**
  - Создать `backend/app/services/email.py`:
    - `async def send_email(to: str, subject: str, html: str) -> bool`:
      1. Использовать `resend` Python SDK.
      2. Отправить письмо с `from=settings.RESEND_FROM_EMAIL`, `to=to`, `subject=subject`, `html=html`.
      3. Вернуть `True` при успехе, `False` при ошибке (логировать ошибку).
      4. Retry: 2 попытки с backoff.
  - Обновить заглушку в `auth.py` ([AUTH]-[001]): заменить print magic link URL на реальную отправку email через `send_email`.

  **Критерии готовности (DoD):**
  - [x] `send_email("test@example.com", "Test", "<h1>Hello</h1>")` отправляет письмо (при валидном API-ключе)
  - [x] При невалидном API-ключе — возвращает `False`, не крашится
  - [x] Magic Link отправляется на email при `POST /api/auth/login`

---

- [x] [NOTIFY]-[002] Создать email-шаблоны (Magic Link, Reminder, Daily Digest)

  **Контекст:** Отправка email работает ([NOTIFY]-[001]). Нужны HTML-шаблоны для 3 типов писем. Стиль: минималистичный, монохромный, в духе Anti-Gamification (PRD §1).

  **Действие:**
  - Создать `backend/app/templates/` директорию.
  - Создать Jinja2-шаблоны (или строки в Python):
    - `magic_link.html`: Заголовок «DD — Your Login Link», кнопка с magic link URL, текст «This link expires in 15 minutes.»
    - `reminder.html`: Заголовок «Time to practice», краткий текст «You have {card_count} words waiting.», кнопка «Open DD».
    - `daily_digest.html`: Заголовок «Your Daily Digest», Traffic Light Report:
      - Для каждого PracticeLog: цветная точка (GREEN/YELLOW/RED) + слово + краткий feedback.
      - GREEN_STAR: выделить похвалой.
      - Ссылка на web app для детального разбора.
      - Текущий streak.
  - Создать `backend/app/services/email.py` — функции-обёртки:
    - `send_magic_link_email(to, url)`
    - `send_reminder_email(to, card_count)`
    - `send_digest_email(to, reviews, streak, app_url)`

  **Критерии готовности (DoD):**
  - [x] 3 HTML-шаблона создано
  - [x] Шаблоны визуально корректны (проверить, открыв HTML в браузере)
  - [x] Функции-обёртки принимают нужные параметры и формируют корректный HTML

---

- [x] [NOTIFY]-[003] Реализовать Smart Nudge (Reminder)

  **Контекст:** PRD §4.4: Smart Nudge — email отправляется через X часов после среднего времени активности пользователя. TECHSPEC §6 Scenario C: Cron каждый час → найти пользователей, которые должны были практиковаться, но не практиковались → отправить напоминание.

  **Действие:**
  - Создать `backend/app/workers/scheduler.py`:
    - `async def smart_nudge_check(ctx)`:
      1. Получить всех пользователей с заполненным `avg_practice_time` и `timezone`.
      2. Для каждого пользователя рассчитать: `nudge_time = avg_practice_time + 1 hour` (в его таймзоне).
      3. Если текущее время в таймзоне пользователя ≈ nudge_time (±30 мин) И пользователь НЕ практиковался сегодня → поставить задачу отправки reminder.
      4. Не отправлять повторно (проверить, что reminder за сегодня не отправлялся — можно хранить дату последнего reminder в Redis или в поле User).
  - Добавить `smart_nudge_check` в расписание Arq (cron: каждый час).
  - Добавить в `backend/app/services/practice.py` обновление `avg_practice_time` при завершении сессии:
    - Rolling average: `new_avg = (old_avg * (n-1) + current_time) / n`, где `n` — количество сессий.
    - Для простоты MVP: просто перезаписывать `avg_practice_time` временем текущей практики.

  **Критерии готовности (DoD):**
  - [x] Cron-задача `smart_nudge_check` запускается каждый час
  - [x] Пользователь получает reminder, если не практиковался и прошёл час после среднего времени
  - [x] Повторный reminder в тот же день не отправляется
  - [x] `avg_practice_time` обновляется при каждой практике

---

- [x] [NOTIFY]-[004] Реализовать Daily Digest (утренний отчёт)

  **Контекст:** LLM-review заполняет `PracticeLog.grade` и `PracticeLog.llm_feedback` ([AI]-[003]). PRD §3.C: Review приходит следующим утром по email (Async Feedback). Traffic Light Report.

  **Действие:**
  - Создать `backend/app/workers/digest.py`:
    - `async def send_daily_digests(ctx)`:
      1. Найти все `PracticeSession` завершённые вчера, у которых `PracticeLog.grade IS NOT NULL` (LLM-review выполнен).
      2. Для каждой сессии собрать данные: список (word, grade, explanation, corrected_sentence, praise).
      3. Получить streak пользователя.
      4. Сформировать HTML через `send_digest_email`.
      5. Отправить email.
  - Добавить `send_daily_digests` в расписание Arq: ежедневно.
  - Логика выбора времени отправки: для MVP — отправлять в 8:00 по таймзоне пользователя (cron каждый час, проверять `user.timezone`).

  **Критерии готовности (DoD):**
  - [x] Cron-задача `send_daily_digests` запускается
  - [x] Пользователь получает digest с Traffic Light Report за вчерашнюю сессию
  - [x] Digest содержит: цветные грейды, слова, feedback, streak, ссылку на приложение
  - [x] Если LLM-review не завершён — digest не отправляется (ждёт)

---

- [x] [NOTIFY]-[099] Уборка этапа NOTIFY

  **Контекст:** Завершены задачи [NOTIFY]-[001]–[NOTIFY]-[004]. Email-система работает: magic link, reminder, digest.

  **Действие:**
  - Проверить, что email-адреса пользователей не логируются в открытом виде (маскировать: `t***@example.com`).
  - Убедиться, что HTML-шаблоны не содержат inline JavaScript (предотвращение XSS в email-клиентах).
  - Проверить, что Resend API-ключ не появляется в логах или error messages.
  - Удалить все print-заглушки, заменить на structured logging.
  - Запустить `ruff check app/workers/ app/services/email.py app/templates/`.

  **Критерии готовности (DoD):**
  - [x] Email-адреса маскированы в логах
  - [x] Нет inline JS в email-шаблонах
  - [x] API-ключи не в логах
  - [x] `ruff check` чисто

---

## Этап 7: UI — Фронтенд PWA

---

- [x] [UI]-[001] Создать Layout и систему роутинга с auth-guard

  **Контекст:** Frontend инициализирован ([INIT]-[004]). Маршруты-заглушки: `/login`, `/capture`, `/practice`, `/history`, `/review`. Zustand для стейта. Auth через JWT Bearer-токен ([AUTH]-[001]).

  **Действие:**
  - Создать `frontend/src/stores/authStore.ts`:
    - Zustand store: `token: string | null`, `user: UserRead | null`, `isAuthenticated: boolean`.
    - Actions: `setToken(token)`, `logout()`, `fetchUser()`.
    - Persist token в `localStorage`.
  - Создать `frontend/src/api/client.ts`:
    - HTTP-клиент (fetch или axios) с базовым URL `/api`.
    - Interceptor: автоматически добавлять `Authorization: Bearer {token}` из authStore.
    - Обработка 401: автоматический logout.
  - Создать `frontend/src/components/Layout.tsx`:
    - Минималистичный layout: header с названием «DD» и streak badge, main content, footer nav (Capture / Practice / History).
    - Монохромный стиль: `bg-white text-gray-900`, `font-sans`.
  - Создать `frontend/src/components/AuthGuard.tsx`:
    - Если `!isAuthenticated` → redirect на `/login`.
    - Иначе → render children.
  - Обновить `App.tsx`: обернуть защищённые маршруты в `AuthGuard`.

  **Критерии готовности (DoD):**
  - [x] Неавторизованный пользователь перенаправляется на `/login`
  - [x] Токен сохраняется в localStorage и восстанавливается при перезагрузке
  - [x] Layout отображается на всех защищённых страницах
  - [x] 401 от API приводит к logout и redirect на `/login`

---

- [x] [UI]-[002] Создать страницу логина (Magic Link)

  **Контекст:** Auth API работает ([AUTH]-[001]): `POST /api/auth/login` → magic link email, `POST /api/auth/verify` → JWT. AuthStore создан ([UI]-[001]).

  **Действие:**
  - Создать `frontend/src/pages/LoginPage.tsx`:
    - Два состояния: «ввод email» и «проверь почту».
    - **Состояние 1:** Поле ввода email (auto-focus), кнопка «Send Magic Link». При submit → `POST /api/auth/login`.
    - **Состояние 2:** Текст «Check your email for a magic link», кнопка «Back».
    - Стиль: центрирован на экране, минимализм, монохром.
  - Создать `frontend/src/pages/AuthVerifyPage.tsx`:
    - URL: `/auth/verify?token=...`
    - При загрузке: взять `token` из query params → `POST /api/auth/verify` → получить `access_token` → `authStore.setToken(token)` → redirect на `/capture`.
    - При ошибке: показать «Link expired or invalid. Try again.» + кнопка на `/login`.
  - Добавить роут `/auth/verify` в `App.tsx`.
  - Создать `frontend/src/api/auth.ts`:
    - `requestMagicLink(email: string)`
    - `verifyToken(token: string)`

  **Критерии готовности (DoD):**
  - [x] Ввод email → нажатие «Send Magic Link» → показ «Check your email»
  - [x] Переход по magic link (`/auth/verify?token=...`) → авторизация → redirect на `/capture`
  - [x] Невалидный/просроченный токен → сообщение об ошибке
  - [x] UI минималистичный, без лишних элементов

---

- [x] [UI]-[003] Создать страницу Capture (ввод нового слова)

  **Контекст:** API: `POST /api/translate` ([CORE]-[002]), `POST /api/cards` ([CORE]-[001]). PRD §3.A & §4.1: пользователь вводит слово → система показывает перевод (Optimistic UI, loading skeleton) → пользователь редактирует/подтверждает → слово сохраняется.

  **Действие:**
  - Создать `frontend/src/pages/CapturePage.tsx`:
    - **Input Field:** Single line, auto-focus, placeholder «Type a word...». Стиль: крупный шрифт, минимализм.
    - При вводе и нажатии Enter (или кнопки):
      1. Немедленно показать карточку со skeleton для перевода.
      2. Вызвать `POST /api/translate` с введённым словом.
      3. Заполнить поле перевода результатом. Если API вернул `null` — показать пустое поле для ручного ввода.
    - **Edit Mode:** Оба поля (слово и перевод) редактируемы. Опциональное поле `context_sentence`.
    - Кнопка «Save» → `POST /api/cards` → показать подтверждение (короткая анимация), очистить форму для следующего слова.
  - Создать `frontend/src/api/cards.ts`:
    - `translateWord(word: string)`
    - `createCard(data: CardCreate)`
    - `getCards(offset, limit)`
  - Создать `frontend/src/stores/captureStore.ts`: состояние формы, loading states.

  **Критерии готовности (DoD):**
  - [x] Ввод слова → loading skeleton → перевод появляется
  - [x] Поля «слово» и «перевод» редактируемы
  - [x] «Save» сохраняет карточку и очищает форму
  - [x] При ошибке API перевода — пустое поле для ручного ввода
  - [x] Auto-focus на поле ввода при загрузке страницы

---

- [x] [UI]-[004] Создать страницу Practice (Zen Mode)

  **Контекст:** API: `GET /api/practice/daily` ([CORE]-[004]), `POST /api/practice/submit` ([CORE]-[005]), `GET /api/cards/:id/translation` ([CORE]-[006]). PRD §3.B & §4.2: строго 10 карточек, Zen Mode (одна карточка на экране), блокировка перехода при пустом поле, кнопка «Reveal Translation».

  **Действие:**
  - Создать `frontend/src/pages/PracticePage.tsx`:
    - При загрузке: `GET /api/practice/daily` → получить 10 карточек.
    - **Zen Mode:** Одна карточка на экране (текущий индекс: 1/10).
    - Содержимое карточки:
      - Слово (крупно).
      - Предыдущее предложение пользователя (если есть) — как «Context Cue» (серым).
      - Поле ввода нового предложения (auto-focus).
      - Кнопка «Reveal Translation» (иконка глаза, скрыта по умолчанию).
    - **Navigation:** Кнопка «Next →» (disabled, пока поле пустое). Нет кнопки «назад» (Zen — только вперёд).
    - **Reveal:** При клике — запрос `GET /api/cards/:id/translation`, показать перевод, отметить `revealed_translation = true` для этой карточки.
    - **Submit:** После 10-й карточки → кнопка «Finish» → `POST /api/practice/submit` со всеми 10 предложениями → показать «Session Complete! Results tomorrow morning.».
    - **Transitions:** Framer Motion — slide-анимация между карточками.
  - Создать `frontend/src/stores/practiceStore.ts`:
    - State: `cards`, `currentIndex`, `sentences: Map<UUID, string>`, `reveals: Map<UUID, boolean>`, `sessionId`.
  - Создать `frontend/src/api/practice.ts`:
    - `getDailyPractice()`
    - `submitPractice(data)`
  - Создать `frontend/src/components/PracticeCard.tsx`: отдельный компонент карточки.

  **Критерии готовности (DoD):**
  - [ ] Показывает одну карточку на экране с номером (1/10)
  - [ ] Нельзя перейти к следующей карточке, пока поле пустое
  - [ ] «Reveal Translation» показывает перевод
  - [ ] После 10-й карточки — «Finish» отправляет все данные
  - [ ] Framer Motion анимация при переключении карточек
  - [ ] Показывается «Session Complete» после submit

---

- [x] [UI]-[005] Создать страницу History (список слов и статистика)

  **Контекст:** API: `GET /api/cards` ([CORE]-[001]), `GET /api/me` ([AUTH]-[003]). Пользователь видит свой словарь и статистику.

  **Действие:**
  - Создать `frontend/src/pages/HistoryPage.tsx`:
    - **Streak Badge:** Крупно показать `streak_current` (число дней), `streak_frozen_count` заморозок.
    - **Word List:** Таблица/список карточек: слово, перевод, вес (визуально — полоска или число), дата добавления.
    - Сортировка: по дате (новые сверху) или по весу (тяжёлые сверху).
    - Пагинация (infinite scroll или кнопка «Load more»).
    - Общая статистика: всего слов, средний вес, дней подряд (streak).
  - Создать `frontend/src/components/StreakBadge.tsx`: компонент отображения стрика.

  **Критерии готовности (DoD):**
  - [x] Страница показывает список всех карточек пользователя
  - [x] Streak отображается крупно
  - [x] Работает сортировка по дате и по весу
  - [x] Пагинация загружает следующие карточки

---

- [x] [UI]-[006] Создать страницу Review (детальный разбор)

  **Контекст:** PRD §3.C: Review — ссылка из Daily Digest ведёт на Web App для детального разбора (Progressive Disclosure). PracticeLog содержит `grade`, `llm_feedback`, `user_sentence`.

  **Действие:**
  - Создать API-эндпоинт (если нет): `GET /api/practice/sessions/{session_id}/review` в backend — возвращает все PracticeLog с grade, feedback, card word.
  - Создать `frontend/src/pages/ReviewPage.tsx`:
    - URL: `/review/:sessionId`.
    - Загрузить данные сессии.
    - Для каждого лога показать:
      - **Traffic Light:** Цветная точка (зелёная/жёлтая/красная) + слово.
      - **GREEN:** Одной строкой — «Correct!».
      - **GREEN_STAR:** С похвалой от AI.
      - **YELLOW:** Предложение пользователя + исправленная версия (diff-подсветка).
      - **RED:** Предложение пользователя + исправленная версия + объяснение ошибки.
  - Создать `frontend/src/components/TrafficLight.tsx`: компонент цветной точки.

  **Критерии готовности (DoD):**
  - [x] Страница загружает и отображает результаты сессии
  - [x] Каждый лог показан с цветовой индикацией (Traffic Light)
  - [x] GREEN_STAR выделен похвалой
  - [x] YELLOW/RED показывают исправления

---

- [x] [UI]-[007] Настроить Service Worker и PWA manifest

  **Контекст:** DD — PWA (PRD §1, TECHSPEC §3). Пользователь должен иметь возможность «установить» приложение на домашний экран. Service Worker кэширует статику.

  **Действие:**
  - Установить `vite-plugin-pwa`:
    ```bash
    npm install -D vite-plugin-pwa
    ```
  - Настроить PWA в `vite.config.ts`:
    ```ts
    import { VitePWA } from "vite-plugin-pwa";
    // в plugins:
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "DD — Daily Dict",
        short_name: "DD",
        description: "The Moleskine for Language Learning",
        theme_color: "#111827",
        background_color: "#ffffff",
        display: "standalone",
        icons: [
          { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
        ],
      },
    })
    ```
  - Создать иконки-заглушки (простые PNG) в `frontend/public/`.
  - Service Worker: кэшировать статические ассеты, API-запросы НЕ кэшировать.

  **Критерии готовности (DoD):**
  - [ ] `manifest.json` генерируется и доступен по `/manifest.json`
  - [ ] Service Worker регистрируется при загрузке приложения
  - [ ] Браузер предлагает «Add to Home Screen» (проверить в Chrome DevTools → Application)
  - [ ] Статические ассеты кэшируются для offline-доступа

---

- [x] [UI]-[099] Уборка этапа UI

  **Контекст:** Завершены задачи [UI]-[001]–[UI]-[007]. Frontend PWA: login, capture, practice, history, review, PWA.

  **Действие:**
  - Удалить неиспользуемые компоненты и страницы-заглушки.
  - Проверить, что все страницы используют единый стиль (монохром, строгая типографика, Tailwind).
  - Убедиться, что нет `console.log` в продакшн-коде.
  - Проверить доступность (a11y): aria-labels на кнопках, semantic HTML, keyboard navigation в Zen Mode.
  - Проверить отзывчивость (responsive): все страницы корректны на мобильных устройствах (375px) и десктопе.
  - Запустить `npm run lint` и `npx prettier --write src/`.

  **Критерии готовности (DoD):**
  - [x] Нет `console.log` в продакшн-коде
  - [x] Все страницы responsive (мобильный + десктоп)
  - [x] Keyboard navigation работает в Practice (Tab, Enter)
  - [x] `npm run lint` и prettier проходят без ошибок

---

## Этап 8: TEST — Тестирование

---

- [x] [TEST]-[001] Настроить тестовую инфраструктуру (conftest, фикстуры, factories)

  **Контекст:** Backend использует Pytest + httpx (async test client), factory_boy для фикстур. БД: PostgreSQL (test database). Нужна изолированная тестовая БД, очищаемая между тестами.

  **Действие:**
  - Создать `backend/tests/conftest.py`:
    - Фикстура `db_session`: создаёт async session к тестовой БД, оборачивает каждый тест в транзакцию и откатывает после.
    - Фикстура `client`: `httpx.AsyncClient` с `app=app` и `base_url="http://test"`.
    - Фикстура `auth_headers(user)`: генерирует JWT для тестового пользователя и возвращает `{"Authorization": "Bearer ..."}`.
    - Фикстура `test_user`: создаёт пользователя через factory.
  - Создать `backend/tests/factories.py`:
    - `UserFactory`: email, timezone, streak defaults.
    - `CardFactory`: word, translation, weight defaults. Зависит от user.
    - `PracticeSessionFactory`, `PracticeLogFactory`.
  - Настроить `DATABASE_URL` для тестов в pyproject.toml или через переменные окружения.

  **Критерии готовности (DoD):**
  - [ ] `pytest tests/` запускается без ошибок (пока 0 тестов)
  - [ ] Фикстуры `db_session`, `client`, `test_user`, `auth_headers` работают
  - [ ] Фабрики создают объекты в тестовой БД
  - [ ] Каждый тест изолирован (транзакция откатывается)

---

- [x] [TEST]-[002] Написать тесты SRS-алгоритма и Streak-логики

  **Контекст:** SRS реализован в `backend/app/services/srs.py` ([CORE]-[003]). Streak — в `backend/app/services/streak.py` ([CORE]-[007]). TECHSPEC §10: тесты `SRS_Algo` и `Streak_Logic`.

  **Действие:**
  - Создать `backend/tests/test_srs.py`:
    - `test_select_cards_weighted`: создать 5 карточек с разными весами (0.01, 0.5, 1.0, 2.0, 5.0), выполнить 1000 выборок, проверить что карточка с весом 5.0 выбирается значительно чаще.
    - `test_weight_update_green`: проверить `weight *= 0.7` при GREEN.
    - `test_weight_update_red`: проверить `weight *= 1.5` при RED.
    - `test_weight_update_green_star`: проверить `weight *= 0.5`, min 0.01.
    - `test_weight_min_clamp`: вес не опускается ниже 0.01.
    - `test_weight_reveal`: проверить `weight *= 2.0` при Reveal.
    - `test_select_fewer_than_10`: если карточек < 10, вернуть все.
  - Создать `backend/tests/test_streak.py`:
    - `test_first_practice`: streak = 1.
    - `test_consecutive_days`: streak растёт 1 → 2 → 3.
    - `test_skip_day_resets`: пропуск → streak = 1.
    - `test_same_day_no_change`: две практики в день → streak не меняется.
    - `test_freeze_preserves_streak`: заморозка спасает стрик.
    - `test_freeze_count_decreases`: `streak_frozen_count` уменьшается при использовании.

  **Критерии готовности (DoD):**
  - [x] Все тесты SRS проходят
  - [x] Все тесты Streak проходят
  - [x] `pytest tests/test_srs.py tests/test_streak.py -v` — зелёный

---

- [x] [TEST]-[003] Написать тесты API-эндпоинтов (Auth, Cards, Practice)

  **Контекст:** API эндпоинты: auth ([AUTH]-[001]), cards ([CORE]-[001]), practice ([CORE]-[004], [CORE]-[005]). TECHSPEC §10: все P0 сценарии должны быть покрыты.

  **Действие:**
  - Создать `backend/tests/test_auth.py`:
    - `test_login_creates_user`: POST /api/auth/login с новым email → 200, пользователь в БД.
    - `test_verify_valid_token`: POST /api/auth/verify → access_token.
    - `test_verify_expired_token`: просроченный magic token → 401.
    - `test_me_authenticated`: GET /api/me с токеном → данные пользователя.
    - `test_me_unauthenticated`: GET /api/me без токена → 401.
  - Создать `backend/tests/test_cards.py`:
    - `test_create_card`: POST /api/cards → 201.
    - `test_list_cards`: GET /api/cards → список карточек текущего пользователя.
    - `test_cards_isolation`: карточки одного пользователя не видны другому.
  - Создать `backend/tests/test_practice.py`:
    - `test_daily_generates_session`: GET /api/practice/daily → 10 карточек.
    - `test_daily_returns_existing_active`: повторный запрос → та же сессия.
    - `test_submit_completes_session`: POST /api/practice/submit → session COMPLETED.
    - `test_submit_wrong_user`: чужая сессия → 403.
    - `test_submit_requires_10_sentences`: меньше 10 → 422.

  **Критерии готовности (DoD):**
  - [x] Все тесты auth проходят
  - [x] Все тесты cards проходят
  - [x] Все тесты practice проходят
  - [x] `pytest tests/ -v` — всё зелёное

---

- [x] [TEST]-[004] Написать тест LLM Worker с мок-ответами

  **Контекст:** LLM Review Worker реализован в `backend/app/workers/llm_review.py` ([AI]-[003]). TECHSPEC §10: `Mock_LLM` — ensure JSON parsing handles malformed LLM responses gracefully.

  **Действие:**
  - Создать `backend/tests/test_llm_review.py`:
    - `test_review_valid_response`: Мокнуть OpenAI API → вернуть корректный JSON → grade и feedback заполнены.
    - `test_review_malformed_json`: Мокнуть OpenAI → вернуть некорректный JSON → grade остаётся None, ошибка залогирована, воркер не упал.
    - `test_review_api_timeout`: Мокнуть OpenAI → timeout → retry 3 раза → graceful failure.
    - `test_review_updates_weight`: После review card.weight обновляется согласно grade.
  - Использовать `unittest.mock.patch` или `pytest-mock` для мока OpenAI.

  **Критерии готовности (DoD):**
  - [x] Все 4 теста проходят
  - [x] Malformed JSON не крашит воркер
  - [x] Timeout приводит к retry, затем graceful failure
  - [x] `pytest tests/test_llm_review.py -v` — зелёный

---

- [x] [TEST]-[099] Уборка этапа TEST

  **Контекст:** Завершены задачи [TEST]-[001]–[TEST]-[004]. Тестовое покрытие: SRS, Streak, Auth, Cards, Practice, LLM Worker.

  **Действие:**
  - Проверить, что все тесты изолированы (не зависят от порядка выполнения).
  - Убедиться, что нет flaky-тестов (запустить `pytest` 3 раза подряд).
  - Проверить, что тесты не используют реальные API-ключи (всё замокано).
  - Удалить дублирование в фикстурах (вынести общие в conftest.py).
  - Убедиться, что CI pipeline ([INIT]-[007]) запускает все тесты.
  - Запустить `ruff check tests/`.

  **Критерии готовности (DoD):**
  - [x] `pytest tests/ -v` — всё зелёное (3 запуска подряд стабильны)
  - [x] Нет реальных API-ключей в тестах
  - [x] Нет дублирования фикстур
  - [x] CI pipeline запускает тесты

---

## Этап 9: SEC — Безопасность

---

- [x] [SEC]-[001] Валидация и санитизация пользовательского ввода

  **Контекст:** TECHSPEC §8: «Sanitize all user inputs (prevent XSS/Injection)». Пользователь вводит: email, слово, перевод, предложения. Все строковые поля проходят через Pydantic, но дополнительная санитизация нужна для HTML/SQL.

  **Действие:**
  - Добавить валидаторы в Pydantic-схемы (`backend/app/schemas/`):
    - `word`: strip whitespace, max length 100, только буквы/цифры/пробелы/дефисы.
    - `translation`: strip, max length 500.
    - `user_sentence`: strip, max length 1000, без HTML-тегов (экранировать `<>`).
    - `context_sentence`: strip, max length 1000, без HTML-тегов.
    - `email`: EmailStr (уже есть), lowercase.
    - `timezone`: проверка через `zoneinfo.ZoneInfo` (уже есть).
  - Создать utility `backend/app/core/sanitize.py`:
    - `def sanitize_text(text: str) -> str`: strip, replace `<` and `>` with entities, collapse whitespace.
  - Применить `sanitize_text` через Pydantic `@field_validator` во всех текстовых полях.

  **Критерии готовности (DoD):**
  - [x] `<script>alert(1)</script>` в поле `word` → экранировано при сохранении
  - [x] Строки длиннее лимита → 422
  - [x] Пустые строки (после strip) → 422
  - [x] SQL-инъекция через строки невозможна (SQLAlchemy параметризует запросы)

---

- [x] [SEC]-[002] Настроить rate limiting

  **Контекст:** TECHSPEC §3: Nginx rate limiting. Дополнительно — SlowAPI на уровне FastAPI для granular control. Критичные эндпоинты: `/api/auth/login` (brute-force magic tokens), `/api/translate` (стоимость API), `/api/practice/submit`.

  **Действие:**
  - Установить `slowapi` в backend:
    ```
    pip install slowapi
    ```
  - Настроить в `backend/app/main.py`:
    - Лимиты по IP: `/api/auth/login` — 5 req/min, `/api/translate` — 20 req/min, остальные — 60 req/min.
    - При превышении → 429 Too Many Requests.
  - В `nginx/nginx.conf` добавить базовый rate limiting:
    ```nginx
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
    limit_req zone=api burst=50 nodelay;
    ```

  **Критерии готовности (DoD):**
  - [x] 6-й запрос на `/api/auth/login` за минуту → 429
  - [x] Nginx rate limiting работает на уровне reverse proxy
  - [x] Лимиты не блокируют нормальное использование (10 submits за сессию проходят)

---

- [x] [SEC]-[003] Настроить CORS, CSP-заголовки, защиту от XSS

  **Контекст:** TECHSPEC §8: HTTPS everywhere, XSS prevention. CORS уже настроен базово ([INIT]-[002]), но нужна доработка.

  **Действие:**
  - Обновить CORS в `main.py`: `allow_origins` только `APP_URL` (не `*`). `allow_credentials=True`.
  - Добавить middleware для Security Headers в `main.py`:
    ```python
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
    ```
  - В `nginx/nginx.conf` добавить CSP header:
    ```nginx
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';" always;
    ```

  **Критерии готовности (DoD):**
  - [x] Запрос с неизвестного origin → CORS reject
  - [x] Response headers содержат X-Frame-Options, X-Content-Type-Options, CSP
  - [x] `curl -I` показывает все security headers

---

- [x] [SEC]-[099] Уборка этапа SEC

  **Контекст:** Завершены задачи [SEC]-[001]–[SEC]-[003]. Безопасность: валидация, rate limiting, headers.

  **Действие:**
  - Провести ручной аудит: пройти по всем эндпоинтам и проверить, что:
    - Каждый protected-эндпоинт требует авторизации.
    - Пользователь не может получить доступ к чужим данным (IDOR check).
    - Все пользовательские строки санитизированы.
  - Проверить `.env.example` — нет ли реальных значений.
  - Проверить, что Docker-образы не содержат `.env` файл (проверить `.dockerignore`).
  - Создать `.dockerignore` в `backend/` и `frontend/`: `.env`, `__pycache__`, `node_modules`, `.git`.

  **Критерии готовности (DoD):**
  - [x] Все protected-эндпоинты проверены на auth
  - [x] IDOR невозможен (пользователь видит только свои данные)
  - [x] `.dockerignore` исключает секреты
  - [x] Нет реальных секретов в `.env.example` и в коде

---

## Этап 10: OPS — Эксплуатация

---

- [x] [OPS]-[001] Настроить structured logging (JSON)

  **Контекст:** TECHSPEC §8: «Structured Logs (JSON) → Local file / Simple viewer». Нужно заменить стандартный uvicorn-лог на JSON-формат для парсинга.

  **Действие:**
  - Установить `structlog` или использовать стандартный `logging` с JSON-форматтером.
  - Создать `backend/app/core/logging.py`:
    - Настроить JSON-форматирование для всех логов.
    - Уровни: DEBUG (dev), INFO (prod).
    - Включить: timestamp, level, logger name, message, extra fields (user_id, request_id).
  - Добавить request_id middleware: генерировать UUID для каждого запроса, прокидывать в логи.
  - Применить logging config при старте приложения в `main.py`.

  **Критерии готовности (DoD):**
  - [x] Логи выводятся в JSON-формате
  - [x] Каждый лог содержит timestamp, level, message
  - [x] Каждый HTTP-запрос имеет уникальный request_id в логах
  - [x] Уровень логирования настраивается через переменную окружения

---

- [x] [OPS]-[002] Интегрировать Sentry для отслеживания ошибок

  **Контекст:** TECHSPEC §8: «Sentry integration for backend errors».

  **Действие:**
  - Установить `sentry-sdk[fastapi]` в backend.
  - Добавить `SENTRY_DSN` в `.env.example` и `Settings`.
  - В `main.py`: инициализировать Sentry при `APP_ENV != "development"`.
    ```python
    if settings.SENTRY_DSN and settings.APP_ENV != "development":
        sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=0.1)
    ```
  - Проверить, что unhandled exceptions отправляются в Sentry.

  **Критерии готовности (DoD):**
  - [x] `SENTRY_DSN` добавлен в `.env.example`
  - [x] Sentry инициализируется только в production
  - [x] Unhandled exception → событие в Sentry (проверить через `sentry_sdk.capture_message("test")`)

---

- [x] [OPS]-[003] Настроить бэкапы PostgreSQL

  **Контекст:** TECHSPEC §4: «Ежесуточный дамп на S3-compatible storage (или локально на VPS с ротацией)». TECHSPEC §8: «Zero data loss for Captured words».

  **Действие:**
  - Создать `scripts/backup.sh`:
    ```bash
    #!/bin/bash
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_DIR="/backups"
    pg_dump -U dd -h db dd | gzip > "$BACKUP_DIR/dd_$TIMESTAMP.sql.gz"
    # Ротация: удалить бэкапы старше 7 дней
    find "$BACKUP_DIR" -name "dd_*.sql.gz" -mtime +7 -delete
    ```
  - Добавить cron в docker-compose.yml (или отдельный контейнер):
    - Запускать `backup.sh` ежедневно в 03:00 UTC.
  - Создать volume для бэкапов в `docker-compose.yml`.

  **Критерии готовности (DoD):**
  - [x] `backup.sh` создаёт gzip-дамп PostgreSQL
  - [x] Ротация удаляет бэкапы старше 7 дней
  - [x] Бэкап восстанавливается: `gunzip < backup.sql.gz | psql -U dd dd` без ошибок

---

- [x] [OPS]-[004] Настроить HTTPS и email-аутентификацию домена

  **Контекст:** TECHSPEC §8: «HTTPS everywhere (LetsEncrypt)». TECHSPEC §11: «Domain authentication (DKIM/SPF) setup is crucial» для email deliverability.

  **Действие:**
  - Обновить `nginx/nginx.conf` для SSL:
    - Добавить certbot-совместимую конфигурацию (http → redirect to https).
    - SSL certificate paths: `/etc/letsencrypt/live/{domain}/`.
  - Добавить `certbot` контейнер в `docker-compose.yml` для автоматического обновления сертификатов.
  - Документировать в README: настройка DNS-записей (A, DKIM, SPF, DMARC) для email-домена.

  **Критерии готовности (DoD):**
  - [x] Nginx конфигурация поддерживает SSL
  - [x] HTTP-запросы перенаправляются на HTTPS
  - [x] Документация по настройке DNS для email

---

- [x] [OPS]-[099] Уборка этапа OPS

  **Контекст:** Завершены задачи [OPS]-[001]–[OPS]-[004]. Логирование, Sentry, бэкапы, HTTPS.

  **Действие:**
  - Проверить, что логи НЕ содержат: пароли, API-ключи, полные email-адреса, JWT-токены.
  - Проверить, что Sentry не отправляет чувствительные данные (настроить `before_send` filter).
  - Убедиться, что `docker-compose.yml` production-ready: все сервисы имеют `restart: unless-stopped`, health checks, resource limits.
  - Проверить, что backup.sh имеет execute permission.
  - Финальный `ruff check` и `npm run lint` на весь проект.

  **Критерии готовности (DoD):**
  - [x] Логи не содержат секретов
  - [x] Sentry фильтрует чувствительные данные
  - [x] Docker-сервисы имеют restart policy и health checks
  - [x] Финальный lint чистый по всему проекту

---

## Контрольная точка: MVP Ready

После выполнения всех этапов (INIT → OPS) проект DD (Daily Dict) готов к запуску MVP:

- **Capture:** Пользователь вводит слово → автоперевод → сохранение карточки.
- **Practice:** 10 карточек/день, Zen Mode, Reveal Translation, Submit.
- **Review:** LLM-проверка предложений, Traffic Light Report, утренний email digest.
- **Streak:** Подсчёт дней подряд, заморозки, No Debt policy.
- **Infra:** Docker, CI/CD, HTTPS, бэкапы, мониторинг.
