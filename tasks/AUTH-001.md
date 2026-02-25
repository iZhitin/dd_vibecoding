# Выполнение задачи [AUTH]-[001]

## Цель:
Реализовать генерацию и отправку Magic Link для бесспарольной аутентификации.

## Что было сделано:
* Создан модуль `app/core/security.py` с функциями генерации стейтлесс JWT-токенов (`create_magic_token`, `verify_magic_token`, `create_access_token`, `verify_access_token`).
* Создан сервис `app/services/auth.py` с функциями для отправки (`request_magic_link`) и валидации (`verify_magic_link`) magic links с созданием пользователей в БД (`AsyncSession`).
* Добавлены роуты `POST /api/auth/login` и `POST /api/auth/verify` в `app/api/routes/auth.py`.
* Настроены unit-тесты в файле `backend/tests/test_auth.py` (с мокированием сессии БД для поддержки `pytest-asyncio`).
* Линтеры (`ruff check`) проверены и исправлены (добавлены `# noqa: B008`, `E501`).

## Решения (ADR):
* Архитектурных изменений не было, логика токенов следует из TECHSPEC.md и реализована с использованием `python-jose`.

## Статус: 
Завершено. Тесты проходят успешно. 
Код готов к коммиту и пушу.
