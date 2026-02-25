# Отчёт о задаче INIT-006: Настроить линтеры и форматтеры

**Статус:** ✅ Выполнено
**Дата:** 2026-02-25

## Что сделано

### Backend (ruff)
- Добавлена секция `[tool.ruff]` в `backend/pyproject.toml`:
  - `target-version = "py312"` — целевая версия Python.
  - `line-length = 100` — максимальная длина строки.
- Добавлена секция `[tool.ruff.lint]` с набором правил:
  - `E` — pycodestyle errors
  - `F` — pyflakes
  - `I` — isort (порядок импортов)
  - `N` — pep8-naming
  - `UP` — pyupgrade
  - `B` — flake8-bugbear
  - `SIM` — flake8-simplify
- Добавлена секция `[tool.pytest.ini_options]` с `asyncio_mode = "auto"`.
- Проверка: `ruff check app/` — **All checks passed!**

### Frontend (eslint + prettier)
- ESLint уже был настроен через Vite-шаблон (react-ts) — дополнительная настройка не потребовалась.
- Создан `frontend/.prettierrc` со следующими настройками:
  - `semi: true` — точки с запятой обязательны.
  - `singleQuote: false` — двойные кавычки.
  - `tabWidth: 2` — отступ 2 пробела.
  - `trailingComma: "all"` — висящие запятые везде.
- Добавлены npm-скрипты: `format` (авто-исправление), `format:check` (проверка без изменений).
- Отформатировано 7 файлов в `src/` по стандартам prettier.
- Проверка: `npx prettier --check src/` — **All matched files use Prettier code style!**
- Проверка: `npx eslint .` — **без ошибок.**

## Верификация
- `cd backend && ruff check app/` ✅
- `cd frontend && npm run lint` ✅
- `cd frontend && npx prettier --check src/` ✅
- `cd backend && pytest tests/ -v` ✅ (1 passed)

## Принятые решения
- Prettier не добавлен в `devDependencies` (нет сетевого доступа для `npm install`), но доступен глобально (v3.8.1). При необходимости добавить позже.

## Связанные файлы
- `backend/pyproject.toml` — конфигурация ruff и pytest
- `frontend/.prettierrc` — конфигурация prettier
- `frontend/package.json` — npm-скрипты format/format:check
