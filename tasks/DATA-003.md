# Задача [DATA]-[003]: Инициализировать Alembic и создать первую миграцию

## Статус
Выполнена

## Контекст
Выполняется настройка базы данных для приложения (миграции). Связанные модели были созданы в рамках `[DATA]-[002]`. В качестве хранилища используется PostgreSQL.

## Что сделано
- Инициализирован alembic с асинхронным шаблоном: `alembic init -t async migrations`. Устаревшая папка от ручного создания удалена перед инициализацией.
- В `alembic.ini` параметр `sqlalchemy.url` зачищен, так как URL задается динамически.
- Изменен файл `backend/migrations/env.py`:
  - В Python `sys.path` добавлен корневой каталог `backend/`, чтобы импорты из `app` работали корректно.
  - Настроен импорт `from app.models import Base` и `from app.core.config import get_settings`.
  - Установлен `target_metadata = Base.metadata` для поддержки autogenerate.
  - Соединение инициализируется через `config.set_main_option("sqlalchemy.url", get_settings().DATABASE_URL)`.
- Сгенерирована начальная миграция: `alembic revision --autogenerate -m "initial schema"`.
- В downgrade скрипт добавлены `DROP TYPE IF EXISTS grade` и `DROP TYPE IF EXISTS sessionstatus` для корректного отката Enum-типов.
- Проведены проверки:
  - `alembic upgrade head` (таблицы созданы).
  - `alembic downgrade base` (таблицы и типы успешно удалены).
  - Повторный `alembic upgrade head` (всё воссоздается без конфликтов).

## Ссылки
- Изменения отражены в `CHANGELOG.md`.
- Задача помечена как выполненная в `BACKLOG.md`.
