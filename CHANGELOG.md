# Changelog — DD (Daily Dict)

Все значимые изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).

---

## [0.1.1] — 2026-02-25

### Добавлено
- **[DATA-001]** Настроен SQLAlchemy async engine и фабрика сессий.
  - Создан `backend/app/core/database.py` (c `create_async_engine`, `async_sessionmaker` и `get_db()`).
  - Создан `backend/app/models/base.py` с базовым классом `Base` и `TimestampMixin`.
- **[INIT-099]** Уборка этапа INIT.
  - Удалены файлы `.gitkeep` из непустых директорий.
  - Из `frontend/` удалены неиспользуемые шаблонные файлы Vite (`App.css`, `react.svg`, `vite.svg`), проверена консистентность конфигурации CORS.
  - Проведена проверка отсутствия захардкоженных секретов в кодовой базе и успешно пройдены линтеры `ruff` и `eslint`.
- **[INIT-007]** Настроен GitHub Actions CI pipeline.
  - Добавлен файл `.github/workflows/ci.yml` с workflow для проверки `main` ветки при `push` и `pull_request`.
  - Включены jobs `backend` (тестирование, линтеры, db+redis) и `frontend` (линтеры, build).
- **[INIT-006]** Настроены линтеры и форматтеры для backend и frontend.
  - Backend: добавлена конфигурация `ruff` в `pyproject.toml` (target Python 3.12, line-length 100, правила E/F/I/N/UP/B/SIM).
  - Backend: добавлена секция `[tool.pytest.ini_options]` с `asyncio_mode = "auto"`.
  - Frontend: создан `.prettierrc` (semicolons, double quotes, trailing commas, tab width 2).
  - Frontend: добавлены npm-скрипты `format` и `format:check` для prettier.
  - Исправлено форматирование 7 файлов в `src/` по стандартам prettier.

---

## [0.1.0] — 2026-02-24

### Добавлено
- **[INIT-001]** Инициализирован Git-репозиторий, создана корневая структура проекта.
- `.gitignore` для Python, Node.js, Docker, IDE.
- `.env.example` со всеми переменными окружения (DB, Redis, JWT, OpenAI, DeepL, Resend, App).
- Полная структура директорий: `backend/` (app, api, models, schemas, services, workers, core, migrations, tests), `frontend/` (src, pages, components, stores, api, lib, public), `nginx/`, `.github/workflows/`.
- Вспомогательные директории `ADR/`, `tasks/` для документирования решений и отчётов о задачах.
- `CHANGELOG.md` для ведения истории изменений.
- **[INIT-002]** Настроен backend: FastAPI + pyproject.toml + точка входа.
- `backend/pyproject.toml` с зависимостями (FastAPI, SQLAlchemy, Pydantic, Arq, OpenAI и др.).
- `backend/app/main.py` — FastAPI app factory с CORS middleware, health-check (`GET /health`), подключёнными роутерами-заглушками (`/api/auth`, `/api/cards`, `/api/practice`, `/api/me`).
- `__init__.py` во всех Python-пакетах (`app`, `api`, `api/routes`, `models`, `schemas`, `services`, `workers`, `core`).
- Роутеры-заглушки: `auth.py`, `cards.py`, `practice.py`, `users.py`.
- **[INIT-003]** Настроена централизованная конфигурация через `pydantic-settings`.
- Добавлен `backend/app/core/config.py` с `Settings(BaseSettings)`, загрузкой `.env` и кэшируемым `get_settings()`.
- `backend/app/main.py` использует `get_settings()` для конфигурации CORS origins через `APP_URL`.
- **[INIT-004]** Настроен frontend на React 18 + Vite + Tailwind CSS + Zustand + Framer Motion.
- Добавлена маршрутизация-заглушка через React Router для путей `/`, `/login`, `/capture`, `/practice`, `/history`, `/review` с редиректом `/ -> /capture`.
- Настроен Tailwind через `@tailwindcss/vite` и `@import "tailwindcss"` в `src/index.css`, добавлены базовые монохромные стили (белый фон, тёмный текст, sans-serif).
- Обновлён `frontend/vite.config.ts`: подключён Tailwind-плагин и proxy `/api` на `http://localhost:8000`.
- Для стабильной верификации тестового контура добавлен backend smoke-тест `backend/tests/test_health.py` (проверка `GET /health`).
- **[INIT-005]** Настроен Docker Compose для локальной разработки и продакшн-шаблона.
- Создан `backend/Dockerfile` (python:3.12-slim).
- Создан `frontend/Dockerfile` (multistage build: node:22-alpine -> nginx:alpine).
- Создан `docker-compose.dev.yml` для запуска PostgreSQL и Redis локально.
- Создан `docker-compose.yml` как шаблон полного стека (backend, frontend, nginx, worker, db, redis).
- Создан `nginx/nginx.conf` с конфигурацией reverse proxy `/api` -> backend, `/` -> frontend.
