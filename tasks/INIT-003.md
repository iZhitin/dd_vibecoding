# [INIT]-[003] Настроить конфигурацию через pydantic-settings

**Статус:** Выполнена  
**Дата:** 2026-02-24

## Что сделано

1. Добавлен `backend/app/core/config.py`:
   - реализован класс `Settings(BaseSettings)` со всеми полями из `.env.example`:
     - `DATABASE_URL`, `REDIS_URL`
     - `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`
     - `OPENAI_API_KEY`, `DEEPL_API_KEY`
     - `RESEND_API_KEY`, `RESEND_FROM_EMAIL`
     - `APP_URL`, `APP_ENV`
   - добавлен `model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")`
   - реализован singleton через `@lru_cache` в `get_settings()`.
2. Обновлён `backend/app/main.py`:
   - подключён `get_settings()` для получения `APP_URL`
   - настроен разбор CORS origins из `APP_URL` (поддержка списка через запятую)
   - добавлен безопасный fallback на `http://localhost:5173`, если origins пустой.
3. Проведена верификация:
   - `ruff check app` — без ошибок
   - проверка загрузки настроек из `.env` через исполняемый smoke-check (`settings_ok`)
   - запуск `uvicorn app.main:app` и запрос `GET /health` → `{"status":"ok"}`.

## Критерии готовности (DoD)

- [x] Создание `.env` с минимальными значениями и запуск `uvicorn` не падает
- [x] `get_settings()` возвращает объект `Settings` с корректными значениями из `.env`

## ADR

Новых архитектурных решений не принималось. Задача реализована в рамках уже выбранного стека и соглашений.
