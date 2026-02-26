# Инструкция по локальному запуску (Development)

Этот документ описывает, как быстро развернуть проект `dd_vibecoding` на локальной машине для разработки (без HTTPS, с доступом по `localhost`).

Проект состоит из четырёх частей:
1. Инфраструктура (PostgreSQL + Redis) — Docker
2. Бэкенд API (FastAPI, Python) — uvicorn
3. Arq-воркер (фоновые задачи: LLM-ревью, дайджесты, напоминания) — arq
4. Фронтенд (React/Vite, TypeScript) — vite

> **Важно:** `.env` файл находится **в корне проекта**. Бэкенд и воркер читают его через симлинк `backend/.env → ../.env`. Если симлинка нет, создайте: `cd backend && ln -sf ../.env .env`

---

## Быстрый старт (все команды)

```bash
# 1. Инфраструктура
docker compose -f docker-compose.dev.yml up -d

# 2. Бэкенд (терминал 1)
cd backend
source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload

# 3. Воркер (терминал 2)
cd backend
source .venv/bin/activate
arq app.workers.config.WorkerSettings

# 4. Фронтенд (терминал 3)
cd frontend
npm run dev
```

После запуска приложение доступно по адресу **http://localhost:5173**

---

## Подробные шаги

### 1. Запуск инфраструктуры (DB + Redis)

```bash
docker compose -f docker-compose.dev.yml up -d
```

> **Не используйте** `docker-compose.yml` (без `.dev`) — он для Production и требует Nginx + SSL.

### 2. Подготовка окружения

Если `.env` ещё нет, скопируйте из примера и заполните ключи:
```bash
cp .env.example .env
```

Необходимые ключи:
| Переменная | Для чего | Обязательно? |
|---|---|---|
| `DEEPL_API_KEY` | Автоперевод слов | Да (или OpenRouter) |
| `OPENROUTER_API_KEY` | LLM-ревью предложений | Да |
| `RESEND_API_KEY` | Отправка email (magic link, дайджест) | Для email-функций |
| `RESEND_FROM_EMAIL` | Адрес отправителя. Для dev: `onboarding@resend.dev` | Если есть Resend |

### 3. Запуск Бэкенда (API-сервер)

```bash
cd backend
python3 -m venv .venv        # только первый раз
source .venv/bin/activate
pip install -e ".[dev]"       # только первый раз
ln -sf ../.env .env           # только первый раз
alembic upgrade head
uvicorn app.main:app --reload
```

Бэкенд будет доступен на `http://localhost:8000`. Magic Link для входа логируется в терминал (ищите `[DEV] Magic link URL:`).

### 4. Запуск Воркера (фоновые задачи)

Воркер **обязателен** для полноценной работы приложения. Без него:
- ❌ Не работает LLM-ревью предложений (оценки GREEN/YELLOW/RED)
- ❌ Не отправляются email-дайджесты
- ❌ Не работают напоминания (smart nudge)

Откройте **отдельный терминал**:
```bash
cd backend
source .venv/bin/activate
arq app.workers.config.WorkerSettings
```

Логи воркера видны прямо в этом терминале.

### 5. Запуск Фронтенда

Откройте **ещё один терминал**:
```bash
cd frontend
npm install                   # только первый раз
npm run dev
```

Фронтенд доступен на **http://localhost:5173**. Запросы к `/api/*` проксируются на бэкенд.

---

## Полезные скрипты

```bash
# Отправить тестовый email-дайджест (без ожидания cron)
cd backend && python -m scripts.send_test_digest

# Проверить LLM-ревью
cd backend && python -m scripts.test_llm_review              # последняя неоценённая сессия
cd backend && python -m scripts.test_llm_review --force       # переоценить последнюю сессию
cd backend && python -m scripts.test_llm_review <session_id>  # конкретная сессия
```

## Остановка

```bash
# Остановить инфраструктуру
docker compose -f docker-compose.dev.yml down

# Остановить бэкенд/воркер/фронтенд — Ctrl+C в соответствующих терминалах
```
