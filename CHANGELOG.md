# Changelog — DD (Daily Dict)

Все значимые изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).

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
