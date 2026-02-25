# Задача [DATA]-[001]: Настроить SQLAlchemy async engine и фабрику сессий

## Статус
Выполнена

## Контекст
Backend настроен ([INIT]-[002]), конфигурация через pydantic-settings ([INIT]-[003]). `DATABASE_URL` доступен через `get_settings().DATABASE_URL`. PostgreSQL запускается через docker-compose.dev.yml.

## Что сделано
- Создан модуль `backend/app/core/database.py`:
  - Настроен `create_async_engine` с параметром `echo=True` (кроме тестов) для вывода SQL-запросов во время разработки.
  - Настроен `async_sessionmaker` для работы с асинхронными сессиями SQLAlchemy.
  - Создана асинхронная генератор-функция `get_db()`, которая предоставляет объект сессии `AsyncSession` с автоматическим `commit()` при успешном выполнении и `rollback()` в случае ошибки, что делает её идеальной для Dependency Injection в FastAPI (через `Depends()`).
- Создан модуль `backend/app/models/base.py`:
  - Определен класс `Base`, наследующийся от `DeclarativeBase` для всех будущих ORM-моделей.
  - Создан `TimestampMixin`, автоматически добавляющий поля `created_at` (записывается при создании) и `updated_at` (обновляется при любых изменениях записи).

## Ссылки
- Изменения отражены в `CHANGELOG.md`.
- Задача помечена как выполненная в `BACKLOG.md`.
