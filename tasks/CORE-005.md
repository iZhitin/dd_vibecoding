# Отчет по задаче [CORE-005]

## Описание задачи
Реализовать POST /api/practice/submit — отправка результатов сессии. Согласно TECHSPEC §6 Scenario B пользователь заполняет 10 предложений → Submit → сервер сохраняет PracticeSession + PracticeLog → запускает LLM-review (асинхронно). Также включена soft-проверка на copy-paste предыдущего ответа (PRD §4.2).

## Что было сделано
1. В `backend/app/services/practice.py` реализована функция `submit_practice`, которая:
   - Находит и валидирует активную сессию пользователя.
   - Проверяет принадлежность каждой карточки пользователю.
   - С помощью `logger.info` записывает soft-check на copy-paste предыдущего ответа.
   - Создает записи `PracticeLog` для выбранных предложений.
   - Увеличивает вес карточки, если пользователь нажал Reveal (`update_weight_after_reveal`).
   - Изменяет статус сессии на `COMPLETED`.
   - Обновляет `last_practice_at` у пользователя.
2. В `backend/app/api/routes/practice.py` добавлен роут `POST /api/practice/submit`.
3. В `backend/tests/test_practice.py` добавлены необходимые фикстуры и тест `test_submit_practice_success` для нового эндпоинта.
4. Исправлены предупреждения `ruff`: организован импорт блоков.

## ADR
Нет новых архитектурных решений.

## Измененные файлы
- `backend/app/services/practice.py`
- `backend/app/api/routes/practice.py`
- `backend/tests/test_practice.py`
- `BACKLOG.md`
- `CHANGELOG.md`
