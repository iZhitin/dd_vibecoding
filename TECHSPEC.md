# TECHSPEC.md — Project DD (Daily Dict)

## 1. Overview
**DD (Daily Dict)** — это минималистичное PWA для осознанной практики иностранного языка (Deliberate Practice). Система фокусируется на активном воспроизведении (написание предложений), асинхронной обратной связи (LLM-review наутро) и жесткой дисциплине (Anti-Gamification).

* **Цель:** Создать надежный инструмент для изучения языка с мгновенным откликом UI и глубокой аналитикой на бэкенде.
* **Ссылки:** [PRD v1.0]

## 2. Scope

### In Scope (MVP)
* **User App (PWA):** Регистрация (Magic Link), Ввод слов (Capture), Практика (10 карт/день), Просмотр истории/статистики.
* **Backend API:** Управление словарем, сессиями практики, подсчет стриков.
* **Background Workers:** Асинхронная проверка предложений (LLM), расчет времени отправки писем (Smart Nudge), отправка Email.
* **Infra:** VPS + Docker Compose + CI/CD (GitHub Actions).

### Out of Scope
* **Admin UI:** Управление пользователями и контентом через прямые запросы к БД.
* **Payments:** Автоматический процессинг донатов (ручная проверка).
* **Social Features:** Лидерборды, друзья, шеринг.
* **Native Mobile Apps:** Только PWA.

### Assumptions
* Пользователь предоставляет свой ключ/оплату для LLM на этапе бета-теста (или мы покрываем расходы из гранта/своих средств). *Риск: Стоимость токенов.*
* VPS (2 vCPU / 4GB RAM) достаточно для MVP нагрузки.

## 3. Architecture

Выбран архитектурный стиль **Modular Monolith** с асинхронными воркерами.

### Components
1.  **Client (PWA):** React (SPA). Работает в браузере, кэширует статику (Service Worker).
2.  **API Gateway / Reverse Proxy:** Nginx (SSL termination, rate limiting).
3.  **Backend Core:** Python (FastAPI). Обрабатывает HTTP-запросы, реализует бизнес-логику (User, Dictionary, Session).
4.  **Task Queue:** Redis. Буфер для "тяжелых" задач (LLM check, Email send) и кэширования сессий.
5.  **Workers:** Celery/Arq. Фоновые процессы:
    * `LLM_Review_Worker`: Валидация предложений.
    * `Scheduler_Worker`: Расчет времени отправки "Smart Nudge".
6.  **Database:** PostgreSQL. Основное хранилище (ACID, Relational).

## 4. Data Model

### Key Entities (ERD Draft)

* **User**
    * `id` (UUID), `email` (Unique), `created_at`
    * `timezone`, `avg_practice_time` (Time), `streak_current`, `streak_frozen_count`
* **Card (Dictionary)**
    * `id`, `user_id` (FK), `word` (Original), `translation`, `context_sentence` (Original context)
    * `srs_level` (float), `next_review_at` (Datetime)
* **PracticeSession**
    * `id`, `user_id` (FK), `started_at`, `completed_at` (Nullable), `status` (active/completed)
* **PracticeLog (Full History)**
    * `id`, `session_id` (FK), `card_id` (FK)
    * `user_sentence` (Input), `llm_feedback` (JSON), `grade` (enum: GREEN/YELLOW/RED)
    * `created_at`

### Storage Strategy
* **Database:** PostgreSQL 16+.
* **Migrations:** Alembic. Версионирование схемы БД обязательно.
* **Backups:** Ежесуточный дамп на S3-compatible storage (или локально на VPS с ротацией).

## 5. Interfaces

### 5.1 External API (Frontend <-> Backend)
*RESTful JSON API.*

* **Auth:** `POST /auth/login` (Magic Link), `POST /auth/verify`.
* **Dictionary:**
    * `POST /cards` (Capture word). *Async translation check.*
    * `GET /cards` (List view).
* **Practice:**
    * `GET /practice/daily` (Generate & Return 10 words). *Stateless.*
    * `POST /practice/submit` (Commit session results).
* **User:**
    * `GET /me` (Stats, Settings).
    * `POST /me/timezone` (Update local time).

### 5.2 Internal Contracts
* **LLM Prompt Schema:** Строгий JSON-формат для ответа LLM (pydantic model), чтобы избежать парсинга текста.
* **Event Bus (Redis):**
    * `task.review_sentence(session_id, inputs[])`
    * `task.send_email(user_id, template_id, context)`

## 6. Workflows (Key Scenarios)

### Scenario A: Capture Word (Optimistic UI)
1.  User types "Serendipity" in PWA.
2.  **UI:** Immediately shows card with loading skeleton for translation.
3.  **API:** `POST /translate` (Background).
4.  **System:** Calls DeepL/Google API.
5.  **UI:** Fills translation field. User accepts or edits.
6.  **API:** `POST /cards` saves final card to DB.

### Scenario B: Daily Practice & Review
1.  User requests `GET /practice/daily`.
2.  **System:** Selects 10 cards based on SRS algorithm (due cards + new cards).
3.  User fills 10 sentences.
4.  User clicks "Submit".
5.  **API:** Saves `PracticeSession` + `PracticeLog` (raw text). Returns "200 OK".
6.  **Worker:** Picks up session. Sends to LLM for review.
7.  **System:** Updates `PracticeLog` with grades. Updates `Card.srs_level`.
8.  **Scheduler:** Updates `User.avg_practice_time` (Rolling Average).

### Scenario C: Smart Nudge
1.  **Cron:** Runs every hour (e.g., at XX:00).
2.  **System:** Finds users where `now() == user.avg_practice_time + 1 hour`.
3.  **Check:** Did user practice today?
    * Yes -> Skip.
    * No -> Enqueue `task.send_email(template="Reminder")`.

## 7. Integrations

| Service | Purpose | Protocol | Fallback Strategy |
| :--- | :--- | :--- | :--- |
| **DeepL / Google API** | Word Translation | REST API | Allow manual user entry if fails. |
| **OpenAI / Anthropic** | Sentence Correction | REST API | Retry x3 with exp. backoff. If dead, save raw logs, review later. |
| **Postmark / SendGrid** | Transactional Email | REST API | Queue & Retry. Log critical failures. |

## 8. Non-Functional Requirements (NFR)

* **Performance:**
    * API Response < 200ms (generic endpoints).
    * Translation < 1s (Async/Optimistic UI covers this).
* **Reliability:**
    * Zero data loss for "Captured" words.
    * Email delivery is critical (Monitor bounce rates).
* **Security:**
    * No passwords stored (Magic Link only).
    * HTTPS everywhere (LetsEncrypt).
    * Sanitize all user inputs (prevent XSS/Injection).
* **Observability:**
    * Structured Logs (JSON) -> Local file / Simple viewer.
    * Sentry integration for backend errors.

## 9. Operations

* **Environment:**
    * **Production:** VPS (Docker Compose).
    * **Secrets:** `.env` file on server (not in Git).
* **CI/CD Pipeline (GitHub Actions):**
    1.  Push to `main`.
    2.  Run `pytest`.
    3.  Build Docker Image -> GHCR.
    4.  SSH to VPS -> `docker compose pull && docker compose up -d`.
* **Database Management:**
    * Manual backups initially.
    * Schema changes via Alembic migrations (part of deploy).

## 10. Testing & Acceptance

* **Strategy:** Backend Integration Tests (Pytest).
* **Key Test Cases:**
    * [Test] `Calculate_Avg_Time`: Ensure rolling average updates correctly.
    * [Test] `SRS_Algo`: Ensure "Review" cards appear before "New" cards.
    * [Test] `Streak_Logic`: Simulate missing a day -> Streak resets.
    * [Test] `Mock_LLM`: Ensure JSON parsing handles malformed LLM responses gracefully.
* **Definition of Done:**
    * All P0 scenarios (Capture, Practice, Review) work.
    * CI pipeline is green.
    * Deploy to VPS is successful.

## 11. Risks & Open Questions

* **Risk:** High cost of LLM tokens if users practice a lot.
    * *Mitigation:* Caching checks for identical sentences; using cheaper models (Haiku/GPT-4o-mini).
* **Risk:** Email deliverability (Spam folder).
    * *Mitigation:* Domain authentication (DKIM/SPF) setup is crucial.
* **Open Question:** "Concierge" recovery process requires SLA. Who is the admin on weekends?

## 12. Backlog Seeds (Epics)

1.  **[Infra] Foundation:** Setup VPS, Docker, CI/CD, DB, Sentry.
2.  **[Core] User & Auth:** Magic Link flow, JWT sessions, User Profile.
3.  **[Core] Capture Engine:** Dictionary API integration, "Card" CRUD, Optimistic UI.
4.  **[Core] Practice Loop:** SRS Logic, Session Generator, "Submit" endpoint.
5.  **[AI] Review Worker:** Async task setup, LLM Prompt Engineering, JSON parsing.
6.  **[Notification] Smart Nudge:** Rolling average logic, Scheduler (Celery Beat), Email templates.
7.  **[Analytics] History & Streak:** Logging system, Streak calculation logic.