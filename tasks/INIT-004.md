# [INIT]-[004] Настроить frontend: React + Vite + Tailwind + Zustand

**Статус:** Выполнена  
**Дата:** 2026-02-24

## Что сделано

1. Инициализирован frontend-проект на Vite (`react-ts`) в каталоге `frontend/`.
2. Установлены зависимости:
   - runtime: `react@18`, `react-dom@18`, `react-router-dom`, `zustand`, `framer-motion`;
   - dev: `tailwindcss`, `@tailwindcss/vite`.
3. Настроен `frontend/vite.config.ts`:
   - подключены плагины `react()` и `tailwindcss()`;
   - добавлен proxy для API: `"/api" -> "http://localhost:8000"`.
4. Реализован базовый роутинг в `frontend/src/App.tsx`:
   - `/` редиректит на `/capture`;
   - добавлены заглушки для `/login`, `/capture`, `/practice`, `/history`, `/review`.
5. Созданы страницы-заглушки в `frontend/src/pages/`:
   - `LoginPage.tsx`, `CapturePage.tsx`, `PracticePage.tsx`, `HistoryPage.tsx`, `ReviewPage.tsx`.
6. Настроен Tailwind и базовый монохромный стиль:
   - в `frontend/src/index.css` добавлен `@import "tailwindcss"`;
   - базовые стили: белый фон, тёмный текст, sans-serif типографика.
7. Дополнительно для прохождения тестового прогона добавлен smoke-тест backend:
   - `backend/tests/test_health.py` проверяет `GET /health` и ответ `{"status": "ok"}`.

## Критерии готовности (DoD)

- [x] `cd frontend && npm run dev` запускает dev-сервер
- [x] `http://localhost:5173` открывается без runtime-ошибок
- [x] Tailwind-классы работают (`text-gray-900` и базовые utility-классы применяются)
- [x] Навигация между маршрутами работает (заглушки)

## Верификация

- `cd frontend && npm run lint` — успешно.
- `cd frontend && npm run build` — успешно.
- Проверка в браузере: открытие `/capture` и переход по ссылкам (`/practice`, и т.д.) — успешно.
- `cd backend && python3.12 -m venv /tmp/dd_backend_venv && source /tmp/dd_backend_venv/bin/activate && python -m pip install ".[dev]" && pytest tests/ -v` — `1 passed`.

## ADR

- [ADR-0001: Bootstrap frontend в INIT-004](../ADR/ADR-0001-init-004-frontend-bootstrap.md)
