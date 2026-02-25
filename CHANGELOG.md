# Changelog — DD (Daily Dict)

Все значимые изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).

---

## [0.1.1] — 2026-02-25

### Добавлено
- **[DATA-099]** Проведена уборка этапа DATA.
  - Проверено единообразное именование моделей (snake_case для полей, PascalCase для классов).
  - Извлечен общий базовый класс `CardBase` для устранения дублирования полей в Pydantic-схемах, относящихся к `Card`.
  - Успешно пройдена проверка `ruff check` для `models/` и `schemas/`.
  - Удостоверено, что `Base.metadata` включает все 4 таблицы.
- **[DATA-005]** Созданы seed-данные для разработки и тестирования.
  - Добавлен скрипт `backend/scripts/seed.py`, который генерирует 1 пользователя (`test@dd.local`), 15 карточек с разными метриками (`weight`, `next_review_at`), 2 сессии и 20 логов (`PracticeLog`).
  - Добавлена команда-синоним `seed` в `pyproject.toml` (`[project.scripts]`).
  - Скрипт поддерживает идемпотентность (старые данные пользователя корректно удаляются перед вставкой новых).
- **[DATA-004]** Созданы Pydantic-схемы (request/response) для всех сущностей (User, Card, Practice, Auth).
  - Настроены параметры `from_attributes=True` для использования SQLAlchemy объектов.
  - Добавлена зависимость `pydantic[email]` в `pyproject.toml`.
- **[DATA-003]** Инициализирован Alembic и создана первая миграция.
  - Установлен асинхронный шаблон Alembic (`alembic init -t async`).
  - Файл `env.py` настроен на использование `Base.metadata` и конфигурации из pydantic-settings.
  - Успешно проверены накатывание (`upgrade head`) и откат (`downgrade base`, с удалением Enum type).
- **[DATA-002]** Созданы SQLAlchemy-модели (User, Card, PracticeSession, PracticeLog).
  - Реализованы таблицы: `users`, `cards`, `practice_sessions`, `practice_logs` со строгой типизацией и использованием UUID.
  - Настроены перечисления (`enum.StrEnum`) для `SessionStatus` и `Grade`.
  - Прописаны связи (`relationship`) и правила каскадного удаления (`cascade="all, delete-orphan"`).
  - Настроен фасад импортов `backend/app/models/__init__.py`.
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

## 2026-02-25
- Выполнена задача **[AUTH-001]**: реализована генерация и отправка Magic Link, настроена генерация JWT и роутинги авторизации.
- Выполнена задача **[AUTH-002]**: реализован middleware (dependency) защиты роутов. Создана функция `get_current_user` (`app/api/deps.py`), извлекающая пользователя из `Bearer` токена.
- Выполнена задача **[AUTH-003]**: реализованы эндпоинты пользователя (`GET /api/me` и `POST /api/me/timezone`), добавлена валидация таймзоны.
- Выполнена задача **[AUTH-099]**: проведена уборка этапа AUTH. Убран дебажный print для URL magic-ссылок, откорректирована конфигурация линтера (добавлено правило `B008` для `fastapi.Depends`), написаны автотесты.
