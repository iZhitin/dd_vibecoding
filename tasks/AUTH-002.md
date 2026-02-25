# [AUTH]-[002] Реализовать middleware защиты роутов (get_current_user)

## Выполненные работы
- Создан модуль `app.api.deps`
- Реализована зависимость `get_current_user`, которая:
  1. Извлекает Bearer token при помощи `OAuth2PasswordBearer`
  2. Валидирует токен функцией `verify_access_token`
  3. Ищет пользователя в БД
  4. Возвращает HTTPException 401, если токен невалиден или пользователь не найден
  5. Возвращает модель `User` при успехе
- Написаны тесты в `backend/tests/test_auth.py`
  - `test_get_current_user_valid`
  - `test_get_current_user_missing_token`
  - `test_get_current_user_invalid_token`
  - `test_get_current_user_not_found`

## Решения (ADR)
Специальных ADR не потребовалось, логика реализована в соответствии с `TECHSPEC.md` и типичными практиками FastAPI (security dependencies).

## Критерии готовности (DoD)
- [x] `get_current_user` корректно извлекает пользователя из Bearer-токена
- [x] Запрос без токена возвращает 401
- [x] Запрос с невалидным токеном возвращает 401
- [x] Запрос с валидным токеном возвращает объект User
