# Changelog — DD (Daily Dict)

Все значимые изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).

---

## [0.1.2] — 2026-02-26

### Добавлено
- **[TEST-002]** Написаны тесты для SRS-алгоритма и Streak-логики.
  - Написаны unit-тесты для SRS (`test_srs.py`): проверено статистическое распределение (Probabilistic Sampling), обновление весов (Green/Red/Green Star), нижняя граница веса и логика расчёта.
  - Написаны unit-тесты для расчёта стрик-логики (`test_streak.py`): первая практика, практика несколько дней подряд, пропуск дней, повторная практика в тот же день, а также заморозка стриков.
- **[TEST-001]** Настроена тестовая инфраструктура (conftest, фикстуры, factories).
  - Настроены асинхронные фикстуры `db_session`, `client`, `auth_headers`, `test_user` в `conftest.py` с автоматическим накатыванием схемы базы данных.
  - Добавлен `factories.py` с фабриками на базе `factory_boy` для всех моделей.
  - Настроено подключение к тестовой БД `dd_test`, проверено прохождение `pytest tests/`.
- **[UI-099]** Проведена уборка этапа UI.
  - Удалены `console.error` из `ReviewPage.tsx` и `HistoryPage.tsx` — продакшн-код не должен содержать console-вызовов.
  - Удалены неиспользуемые каталоги `src/assets/` (пустой) и `src/lib/` (только `.gitkeep`).
  - Удалён артефактный CSS-класс `border-red-500` в PracticePage.
  - Добавлена доступность (a11y): `aria-label` на все кнопки (Reveal, Next/Finish, Logout, Load More, Try Again и др.),  `role="img"` и `aria-label` в `TrafficLight`, `aria-label="Main navigation"` на `<nav>`.
  - Проверена работа keyboard navigation в Practice (Tab/Enter), responsive-вёрстка на мобильных (375px).
  - Запущены и пройдены `npm run lint`, `prettier --check`, `npm run build`, все 32 backend-теста.
- **[UI-007]** Настроен Service Worker и PWA manifest.
  - Сгенерированы минималистичные монохромные иконки приложения (512, 192, 180, 32, 16 px).
  - Расширена конфигурация `vite-plugin-pwa`: `start_url`, `scope`, maskable icon, Workbox с `navigateFallbackDenylist` для исключения `/api` из кэша SW.
  - Обновлён `index.html`: добавлены PWA meta-теги (`theme-color`, `description`), `apple-touch-icon`, favicon PNG.
  - Статические ассеты кэшируются для offline-доступа, API-запросы не кэшируются.

---

## [0.1.1] — 2026-02-25

### Добавлено
- **[DATA-099]** Проведена уборка этапа DATA.
  - Проверено единообразное именование моделей (snake_case для полей, PascalCase для классов).
  - Извлечен общий базовый класс `CardBase` для устранения дублирования полей в Pydantic-схемах, относящихся к `Card`.
  - Успешно пройдена проверка `ruff check` для `models/` и `schemas/`.
  - Удостоверено, что `Base.metadata` включает все 4 таблицы.
- **[DATA-005]** Созданы seed-данные для разработки и тестирования.
  - Добавлен скрипт `backend/scripts/seed.py`, который генерирует 1 пользователя (`test@dd.local`), 15 карточек с разными метриками (`weight`, `next_review_at`), 2 сессии и 20 логов (`PracticeLog`).
  - Добавлена команда-синоним `seed` в `pyproject.toml` (`[project.scripts]`).
  - Скрипт поддерживает идемпотентность (старые данные пользователя корректно удаляются перед вставкой новых).
- **[DATA-004]** Созданы Pydantic-схемы (request/response) для всех сущностей (User, Card, Practice, Auth).
  - Настроены параметры `from_attributes=True` для использования SQLAlchemy объектов.
  - Добавлена зависимость `pydantic[email]` в `pyproject.toml`.
- **[DATA-003]** Инициализирован Alembic и создана первая миграция.
  - Установлен асинхронный шаблон Alembic (`alembic init -t async`).
  - Файл `env.py` настроен на использование `Base.metadata` и конфигурации из pydantic-settings.
  - Успешно проверены накатывание (`upgrade head`) и откат (`downgrade base`, с удалением Enum type).
- **[DATA-002]** Созданы SQLAlchemy-модели (User, Card, PracticeSession, PracticeLog).
  - Реализованы таблицы: `users`, `cards`, `practice_sessions`, `practice_logs` со строгой типизацией и использованием UUID.
  - Настроены перечисления (`enum.StrEnum`) для `SessionStatus` и `Grade`.
  - Прописаны связи (`relationship`) и правила каскадного удаления (`cascade="all, delete-orphan"`).
  - Настроен фасад импортов `backend/app/models/__init__.py`.
- **[DATA-001]** Настроен SQLAlchemy async engine и фабрика сессий.
  - Создан `backend/app/core/database.py` (c `create_async_engine`, `async_sessionmaker` и `get_db()`).
  - Создан `backend/app/models/base.py` с базовым классом `Base` и `TimestampMixin`.
- **[INIT-099]** Уборка этапа INIT.
  - Удалены файлы `.gitkeep` из непустых директорий.
  - Из `frontend/` удалены неиспользуемые шаблонные файлы Vite (`App.css`, `react.svg`, `vite.svg`), проверена консистентность конфигурации CORS.
  - Проведена проверка отсутствия захардкоженных секретов в кодовой базе и успешно пройдены линтеры `ruff` и `eslint`.
- **[INIT-007]** Настроен GitHub Actions CI pipeline.
  - Добавлен файл `.github/workflows/ci.yml` с workflow для проверки `main` ветки при `push` и `pull_request`.
  - Включены jobs `backend` (тестирование, линтеры, db+redis) и `frontend` (линтеры, build).
- **[INIT-006]** Настроены линтеры и форматтеры для backend и frontend.
  - Backend: добавлена конфигурация `ruff` в `pyproject.toml` (target Python 3.12, line-length 100, правила E/F/I/N/UP/B/SIM).
  - Backend: добавлена секция `[tool.pytest.ini_options]` с `asyncio_mode = "auto"`.
  - Frontend: создан `.prettierrc` (semicolons, double quotes, trailing commas, tab width 2).
  - Frontend: добавлены npm-скрипты `format` и `format:check` для prettier.
  - Исправлено форматирование 7 файлов в `src/` по стандартам prettier.

---

## [0.1.0] — 2026-02-24

### Добавлено
- **[INIT-001]** Инициализирован Git-репозиторий, создана корневая структура проекта.
- `.gitignore` для Python, Node.js, Docker, IDE.
- `.env.example` со всеми переменными окружения (DB, Redis, JWT, OpenAI, DeepL, Resend, App).
- Полная структура директорий: `backend/` (app, api, models, schemas, services, workers, core, migrations, tests), `frontend/` (src, pages, components, stores, api, lib, public), `nginx/`, `.github/workflows/`.
- Вспомогательные директории `ADR/`, `tasks/` для документирования решений и отчётов о задачах.
- `CHANGELOG.md` для ведения истории изменений.
- **[INIT-002]** Настроен backend: FastAPI + pyproject.toml + точка входа.
- `backend/pyproject.toml` с зависимостями (FastAPI, SQLAlchemy, Pydantic, Arq, OpenAI и др.).
- `backend/app/main.py` — FastAPI app factory с CORS middleware, health-check (`GET /health`), подключёнными роутерами-заглушками (`/api/auth`, `/api/cards`, `/api/practice`, `/api/me`).
- `__init__.py` во всех Python-пакетах (`app`, `api`, `api/routes`, `models`, `schemas`, `services`, `workers`, `core`).
- Роутеры-заглушки: `auth.py`, `cards.py`, `practice.py`, `users.py`.
- **[INIT-003]** Настроена централизованная конфигурация через `pydantic-settings`.
- Добавлен `backend/app/core/config.py` с `Settings(BaseSettings)`, загрузкой `.env` и кэшируемым `get_settings()`.
- `backend/app/main.py` использует `get_settings()` для конфигурации CORS origins через `APP_URL`.
- **[INIT-004]** Настроен frontend на React 18 + Vite + Tailwind CSS + Zustand + Framer Motion.
- Добавлена маршрутизация-заглушка через React Router для путей `/`, `/login`, `/capture`, `/practice`, `/history`, `/review` с редиректом `/ -> /capture`.
- Настроен Tailwind через `@tailwindcss/vite` и `@import "tailwindcss"` в `src/index.css`, добавлены базовые монохромные стили (белый фон, тёмный текст, sans-serif).
- Обновлён `frontend/vite.config.ts`: подключён Tailwind-плагин и proxy `/api` на `http://localhost:8000`.
- Для стабильной верификации тестового контура добавлен backend smoke-тест `backend/tests/test_health.py` (проверка `GET /health`).
- **[INIT-005]** Настроен Docker Compose для локальной разработки и продакшн-шаблона.
- Создан `backend/Dockerfile` (python:3.12-slim).
- Создан `frontend/Dockerfile` (multistage build: node:22-alpine -> nginx:alpine).
- Создан `docker-compose.dev.yml` для запуска PostgreSQL и Redis локально.
- Создан `docker-compose.yml` как шаблон полного стека (backend, frontend, nginx, worker, db, redis).
- Создан `nginx/nginx.conf` с конфигурацией reverse proxy `/api` -> backend, `/` -> frontend.

## 2026-02-25
- Выполнена задача **[AUTH-001]**: реализована генерация и отправка Magic Link, настроена генерация JWT и роутинги авторизации.
- Выполнена задача **[AUTH-002]**: реализован middleware (dependency) защиты роутов. Создана функция `get_current_user` (`app/api/deps.py`), извлекающая пользователя из `Bearer` токена.
- Выполнена задача **[AUTH-003]**: реализованы эндпоинты пользователя (`GET /api/me` и `POST /api/me/timezone`), добавлена валидация таймзоны.
- Выполнена задача **[AUTH-099]**: проведена уборка этапа AUTH. Убран дебажный print для URL magic-ссылок, откорректирована конфигурация линтера (добавлено правило `B008` для `fastapi.Depends`), написаны автотесты.
- Выполнена задача **[CORE-001]**: реализованы POST и GET эндпоинты API карточек с поддержкой пагинации и создания новой карточки. Автоматически проставляется `weight = 1.0` и `next_review_at` для новых карточек. Написаны тесты, линтеры проходят без замечаний.
- Выполнена задача **[CORE-002]**: реализована функция автоперевода с использованием DeepL API с fallback на OpenAI gpt-4o-mini. Добавлен защищенный эндпоинт `POST /api/translate`. Написаны unit-тесты.
- Выполнена задача **[CORE-003]**: реализован SRS-алгоритм (Probabilistic Sampling) с выборкой карточек пропорционально их весу и логикой корректировки веса по результатам практики. Написаны тесты с проверкой статистического распределения.
- Выполнена задача **[CORE-004]**: реализована генерация ежедневной сессии практики на 10 карточек с подгрузкой контекста предыдущего предложения. Создан защищенный эндпоинт `GET /api/practice/daily`.
- Выполнена задача **[CORE-005]**: реализован POST /api/practice/submit для отправки результатов сессии. Записываются PracticeLog, обновляется last_practice_at у пользователя, сессия помечается COMPLETED. Включена soft-проверка на copy-paste предыдущего ответа. Добавлены тесты.
- Выполнена задача **[CORE-006]**: реализован GET /api/cards/{card_id}/translation эндпоинт для получения перевода карточки пользователем. Написаны тесты, линтеры проходят без замечаний.
- Выполнена задача **[CORE-007]**: реализована логика расчета стриков (пропуск дня, отскок стрика, заморозки) с учетом часового пояса пользователя. Логика интегрирована в `submit_practice`.
- Выполнена задача **[CORE-099]**: проведен этап уборки слоя CORE. Решены проблемы N+1 запросов в `practice_services` при помощи массовой загрузки данных об активностях и `DISTINCT ON`. Захардкоженные магические числа для множителей SRS перемещены в именованные константы. Успешно пройдены проверки `pytest` и `ruff`.
- Выполнена задача **[AI-001]**: настроен Arq worker с подключением к Redis для обработки асинхронных задач LLM. 
- Выполнена задача **[AI-002]**: создана Pydantic-схема `SessionReviewResponse` для строгого LLM-ответа формата Traffic Light Report (оценка, похвала, пояснение и корректировка).
- Выполнена задача **[AI-003]**: реализован LLM Review Worker c запросами к OpenAI (model=gpt-4o-mini, response_format), механизмом exponential backoff на 3 попытки, и обновлением JSONB полей. Расчёт веса карточек синхронизирован с SRS-алгоритмом.
- Выполнена задача **[AI-004]**: подключён `enqueue_job` для асинхронной задачи проверки к `submit_practice`.
- Выполнена задача **[AI-099]**: проведена уборка слоя AI. Проверен маскинг OpenAI_API_KEY, gracefully обработаны пустые ключи и fallback-сценарии. Исходный код почищен линтерами.
- Выполнена задача **[NOTIFY-001]**: интегрирован почтовый клиент Resend для отправки email. Создан сервис email с поддержкой retry backoff, обновлена отправка Magic Link при авторизации.
- Выполнена задача **[NOTIFY-002]**: созданы HTML-шаблоны писем (Magic Link, Reminder, Daily Digest) с монохромным минималистичным дизайном. Для шаблонизации использован встроенный `.format()` без добавления зависимости Jinja2. Созданы функции-обёртки для удобной отправки писем.
- Выполнена задача **[NOTIFY-003]**: реализована логика Smart Nudge. Создан воркер `scheduler.py` с крон-задачей `smart_nudge_check`, запускаемой каждый час, которая проверяет потребность отправки email-напоминаний с учетом `avg_practice_time` и часового пояса пользователей. Для предотвращения дубликации использован кеш в Redis. При успешном завершении ежедневной практики обновляется `avg_practice_time`.
- Выполнена задача **[NOTIFY-004]**: реализован Daily Digest (утренний отчёт). Добавлена cron-задача `send_daily_digests` на базе Arq_workers, которая в локальные 8:00 утра для пользователя отправляет email с отчетом Traffic Light Report за вчерашнюю практику. Выполняется проверка готовности LLM-ревью перед отправкой, применяется Redis caching для идемпотентности, и используется HTML шаблон `send_digest_email`.
- Выполнена задача **[NOTIFY-099]**: проведена уборка этапа NOTIFY. Маскированы email-адреса в логах (`t***@example.com`), убраны сенситивные данные из логов (URL-ссылки), проверено отсутствие inline JS в шаблонах писем и API-ключей в логах, исходный код очищен и исправлены ошибки линтера.
- Выполнена задача **[UI-001]**: создан Layout мобильного приложения и система роутинга с auth-guard. Добавлены базовые роуты, Zustand store для хранения токена через localStorage, fetch-клиент с обработкой 401 Unauthorized, а также компоненты `AuthGuard`, `GuestGuard` и `Layout`.
- Выполнена задача **[UI-002]**: создана страница логина (`LoginPage`) с отправкой Magic Link на email и страница верификации ссылок (`AuthVerifyPage`). Добавлен HTTP-клиент для взаимодействия с Auth API. Обновлен роутер приложения.
- Выполнена задача **[UI-003]**: создана страница Capture (`CapturePage`). Реализовано сохранение новых слов с автопереводом. Автоперевод сделан по принципу Optimistic UI через эндпоинт `/api/translate` с поддержкой редактирования ручного перевода. Добавлены красивый скелетон и анимации через `framer-motion`. Стейт страницы вынесен в хук Zustand `useCaptureStore`.
- Выполнена задача **[UI-004]**: создана страница Practice (Zen Mode) (`PracticePage`). Карточка практики выделена в отдельный компонент (`PracticeCard.tsx`), а стейт сессии вынесен в `usePracticeStore.ts` (Zustand). Добавлены slide-анимации через `framer-motion`, реализовано открытие перевода по кнопке (Reveal Translation) и блокировка перехода при пустом поле.
- Выполнена задача **[UI-005]**: создана страница History (список слов и статистика) (`HistoryPage`). Сделана пагинация карточек с использованием `loadMore`, возможность изменять глобальную сортировку слов "по новизне" или "по весу". Выделен компонент `StreakBadge` для крупного отображения прогресса пользователя, API расширено параметром `sort_by`.
- Выполнена задача **[UI-006]**: создана страница Review (детальный разбор) (`ReviewPage.tsx`). Загружает данные завершенной сессии, отображает каждый лог с цветовой индикацией Traffic Light. GREEN_STAR выделен похвалой от модели, YELLOW и RED показывают исправления с объяснениями. В API создан соответствующий эндпоинт загрузки данных.
