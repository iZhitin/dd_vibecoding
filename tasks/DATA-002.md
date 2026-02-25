# Задача [DATA]-[002]: Создать SQLAlchemy-модели: User, Card, PracticeSession, PracticeLog

## Статус
Выполнена

## Контекст
База и миксины созданы в рамках задачи [DATA]-[001]. Модель данных основана на PRD §6 (приоритет) и TECHSPEC §4 (детали).

## Что сделано
- Созданы базовые SQLAlchemy модели:
  - `User` (`backend/app/models/user.py`): хранит email, timezone, среднее время практики (avg_practice_time), стрики и статус заморозки. Имеет связи к карточкам и сессиям.
  - `Card` (`backend/app/models/card.py`): хранит слово, перевод, контекстуальное предложение, вес (weight для SRS, default = 1.0) и следующее время для обзора (next_review_at).
  - `PracticeSession` (`backend/app/models/practice_session.py`): хронология и статус сессии пользователя. Содержит Enum `SessionStatus`.
  - `PracticeLog` (`backend/app/models/practice_log.py`): детализация каждого ответа пользователя в рамках сессии. Хранит Enum `Grade` (GREEN, GREEN_STAR, YELLOW, RED), пользовательское предложение и JSON с фидбеком от LLM.
- Организованы двунаправленные связи (`relationship`) с настройкой каскадного удаления (`cascade="all, delete-orphan"`).
- Строгие перечисления (`enum.StrEnum`) добавлены для `SessionStatus` и `Grade`.
- Добавлен и экспортирован импорт моделей через `backend/app/models/__init__.py`.
- Код автоматически отформатирован и проверен линтером `ruff`, исправлены проблемы с типизацией и цикличными зависимостями (`TYPE_CHECKING`).

## Ссылки
- Изменения отражены в `CHANGELOG.md`.
- Задача помечена как выполненная в `BACKLOG.md`.
