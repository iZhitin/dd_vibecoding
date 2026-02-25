# [AUTH]-[003] Реализовать эндпоинт GET /api/me и POST /api/me/timezone

## Выполненные работы
- Создан роутер `api/routes/users.py`
- Реализован эндпоинт `GET /api/me`: возвращает `UserRead` для `current_user` (с использованием `Depends(get_current_user)`)
- Реализован эндпоинт `POST /api/me/timezone`: валидирует таймзону (через схему `TimezoneUpdate`), обновляет её у пользователя в БД и возвращает пользователя 
- Роутер подключен к основному приложению в `main.py`
- Добавлены автотесты в `backend/tests/test_users.py` на успешные и ошибочные сценарии
- Убраны лишние импорты (lint fixed, bugbear rule in pyproject.toml)

## Решения (ADR)
Для проверки IANA timezone мы используем встроенный модуль питона `zoneinfo` (`available_timezones()`), что соответствует современным стандартам работы со временем в Python 3.9+.

## Критерии готовности (DoD)
- [x] `GET /api/me` с валидным токеном возвращает данные пользователя
- [x] `POST /api/me/timezone` с `{"timezone": "Europe/Berlin"}` обновляет таймзону
- [x] Невалидная таймзона (например, `"Mars/Olympus"`) возвращает 422
