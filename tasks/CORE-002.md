# Отчёт о задаче CORE-002

## Задача
Интегрировать Dictionary API для автоперевода

## Изменения
- Созданы Pydantic-схемы `TranslateRequest` и `TranslateResponse` (`backend/app/schemas/translate.py`).
- Создан модуль логики `backend/app/services/translation.py`, реализующий запрос в DeepL (приоритет) с fallback-логикой на OpenAI gpt-4o-mini. Третий вариант - возврат значения null.
- Настроен таймаут на 5 секунд в обоих HTTP-клиентах.
- Подключен маршрут `POST /api/translate` для автотрансляции введенного слова, внедрен в общую схему FastAPI (`backend/app/main.py`).
- Тесты написаны в `backend/tests/test_translate.py` (используется mock для `httpx` и `AsyncOpenAI`). Имитируется поведение DeepL, OpenAI, и ситуации отказа обоих сервисов (возвращается timeout).

## DoD выполнено полностью
- `POST /api/translate` с `{"word": "hello"}` возвращает перевод (при наличии API ключа)
- При недоступности API возвращает `{"translation": null}` (не 500)
- Timeout не превышает 5 секунд (внедрено в `async_with`)
- Линтеры `ruff` успешно пройдены

## Ссылки на ADR
Не принимались новые архитектурные решения.
