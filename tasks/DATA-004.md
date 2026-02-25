# Отчёт по задаче [DATA]-[004]

## Описание
Создание Pydantic-схем (request/response) для всех сущностей (User, Card, Practice, Auth).

## Выполненная работа
- Созданы схемы аутентификации в `backend/app/schemas/auth.py`: `LoginRequest`, `VerifyRequest`, `TokenResponse`.
- Созданы схемы для карточек в `backend/app/schemas/card.py`: `CardCreate`, `CardRead`, `CardList`. Настроен `ConfigDict(from_attributes=True)` для `CardRead`.
- Созданы схемы для практики в `backend/app/schemas/practice.py`: `PracticeCardRead`, `DailyPracticeResponse`, `SentenceSubmit`, `PracticeSubmitRequest`. Добавлена валидация на ожидаемые 10 карточек в `PracticeSubmitRequest`. 
- Созданы схемы для пользователя в `backend/app/schemas/user.py`: `UserRead`, `TimezoneUpdate`. Добавлена валидация `timezone` по IANA timezones через `zoneinfo`.
- Все схемы импортированы и открыты через `backend/app/schemas/__init__.py`.
- Произведена установка `pydantic[email]` (и `email-validator`) для работы `EmailStr`. Зависимость обновлена в `pyproject.toml`.
- Код отформатирован с помощью линтера `ruff`. 

## Принятые решения (ADR)
Не требуется: все схемы созданы строго в соответствии с PRD и TECHSPEC без введения новых архитектурных решений.

## Критерии готовности (DoD)
- [x] Все схемы импортируются без ошибок.
- [x] `PracticeSubmitRequest` отклоняет payload с количеством sentences != 10.
- [x] `CardRead` корректно сериализует SQLAlchemy-модель.
