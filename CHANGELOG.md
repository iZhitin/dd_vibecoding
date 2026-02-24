# Changelog — DD (Daily Dict)

Все значимые изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).

---

## [0.1.0] — 2026-02-24

### Добавлено
- **[INIT-001]** Инициализирован Git-репозиторий, создана корневая структура проекта.
- `.gitignore` для Python, Node.js, Docker, IDE.
- `.env.example` со всеми переменными окружения (DB, Redis, JWT, OpenAI, DeepL, Resend, App).
- Полная структура директорий: `backend/` (app, api, models, schemas, services, workers, core, migrations, tests), `frontend/` (src, pages, components, stores, api, lib, public), `nginx/`, `.github/workflows/`.
- Вспомогательные директории `ADR/`, `tasks/` для документирования решений и отчётов о задачах.
- `CHANGELOG.md` для ведения истории изменений.
