# [INIT]-[001] Создать корневую структуру проекта и Git-репозиторий

**Статус:** Выполнена
**Дата:** 2026-02-24

## Что сделано

1. Инициализирован Git-репозиторий в корне проекта.
2. Создан `.gitignore` с правилами для Python (`__pycache__`, `.venv`, `.pytest_cache`, `*.pyc`), Node.js (`node_modules`), Docker, IDE (`.idea`, `.vscode`), OS-файлов и `.env`.
3. Создан `.env.example` со всеми переменными окружения: `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`, `OPENAI_API_KEY`, `DEEPL_API_KEY`, `RESEND_API_KEY`, `RESEND_FROM_EMAIL`, `APP_URL`, `APP_ENV`.
4. Созданы все директории из эталонной структуры проекта с `.gitkeep`:
   - `backend/app/{api/routes, models, schemas, services, workers, core}`
   - `backend/{migrations/versions, tests}`
   - `frontend/src/{pages, components, stores, api, lib}`
   - `frontend/public`
   - `nginx`
   - `.github/workflows`
5. Созданы вспомогательные директории `ADR/`, `tasks/` и файл `CHANGELOG.md`.

## Критерии готовности (DoD)

- [x] Git-репозиторий инициализирован, `.gitignore` корректно игнорирует лишние файлы
- [x] `.env.example` содержит все перечисленные переменные
- [x] Все директории из эталонной структуры существуют

## ADR

Нет принятых архитектурных решений — задача чисто инфраструктурная.
