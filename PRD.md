# Product Requirements Document (PRD)
## Project: DD (Daily Dict)
**Version:** 1.0 (MVP)
**Status:** Approved for Development
**Date:** February 2026
**Role:** World-Class Product Architect

---

### 1. Vision & Core Philosophy
**"The Moleskine for Language Learning"**
DD — это минималистичный PWA-инструмент для осознанной практики (Deliberate Practice) иностранного языка. В отличие от Duolingo (где обучение пассивно), DD требует когнитивного усилия: пользователь сам находит слова и сам пишет предложения.

* **Anti-Gamification:** Мы не развлекаем пользователя. Мы даем ему инструмент для работы.
* **High Friction, High Reward:** Усилие при вводе — залог запоминания.
* **Async Feedback:** Мгновенная валидация убивает поток. Анализ ошибок приходит наутро.

### 2. Target Audience
**Primary Persona:** "The Deliberate Learner"
* **Уровень:** B1+ (может строить предложения самостоятельно).
* **Боли:** Duolingo слишком легкий; слова из книг/статей записываются в заметки и умирают там.
* **Контекст:** Готов тратить 5-10 минут в день на глубокую работу (Deep Work).

---

### 3. User Journey (The Core Loop)

#### A. Capture (Захват)
1.  **Trigger:** Пользователь встречает новое слово в жизни (книга, фильм, разговор).
2.  **Action:** Открывает DD (PWA) -> Вводит слово.
3.  **System Response:**
    * Делает запрос к внешнему API (Dictionary).
    * Предлагает перевод/определение.
4.  **User Validation:** Пользователь **редактирует** или подтверждает перевод (Critical Step: присвоение смысла).
5.  **Result:** Слово попадает в "Inbox".

#### B. Daily Practice (Практика)
1.  **Trigger:** Email-напоминание (Smart Nudge) в привычное время пользователя.
2.  **Session:** Строго 10 карточек (Zen Mode).
3.  **Interaction Flow:**
    * Экран показывает **только** одну карточку.
    * **Стимул:** Видит свое старое предложение (Context Cue).
    * **Задача:** Написать *новое* предложение с этим словом.
    * **Hardcore Modifier:** Если уровень слова высокий, система предлагает "Combo Mode" (использовать текущее слово + случайное слово из базы).
    * **Help:** Кнопка "Reveal Translation" (снижает рейтинг знания, но помогает продолжить).
4.  **Completion:** Сессия завершена. Данные уходят на сервер.

#### C. Review (Обратная связь)
1.  **Timing:** Следующее утро (Async).
2.  **Channel:** Email Briefing ("Daily Digest").
3.  **Content:**
    * **Traffic Light Report:**
        * 🟢 **Green:** Без ошибок (одной строкой).
        * 🌟 **Green+:** Выдающееся использование (с похвалой от AI).
        * 🟡 **Yellow:** Мелкие недочеты (стиль, опечатка).
        * 🔴 **Red:** Грамматическая ошибка (требует внимания).
    * **Action:** Ссылка на Web App для детального разбора (Progressive Disclosure).

---

### 4. Functional Requirements

#### 4.1. Capture Interface
* **Input Field:** Single line, auto-focus, fast load.
* **Enrichment:** Интеграция с Dictionary API (Google Translate / OpenAI / Linguee).
* **Edit Mode:** Полный контроль пользователя над полями "Слово" и "Перевод".

#### 4.2. Practice Engine
* **Batch Size:** Строго 10 слов.
* **Navigation:** Zen Mode (одна карточка на экране). Блокировка перехода, пока поле ввода пустое.
* **Context Display:**
    * Приоритет 1: Предыдущее предложение пользователя (показано явно как основной стимул).
    * Приоритет 2: Перевод (скрыт под кнопкой).
* **Uniqueness Check:** (Soft) Проверка на copy-paste предыдущего ответа.

#### 4.3. Intelligent Scheduling (Invisible SRS)
* **Algorithm:** Вероятностная выборка (Probabilistic Sampling), а не жесткие интервалы.
* **Signals:**
    * Нажатие "Reveal Translation" -> Вес слова резко растет (чаще показываем).
    * Ошибка в предложении (AI Review) -> Вес растет.
    * Успех -> Вес снижается (но не до 0, min 0.01%).
* **Graduation:** Нет "архива". Слово навсегда остается в длинном хвосте (Infinite Tail).

#### 4.4. Streak & Recovery Logic
* **Policy:** No Debt. Пропущенные дни сгорают.
* **Recovery:** "Concierge Model" (MVP).
    * Пользователь переводит донат вручную (карта/кошелек).
    * Отправляет ID транзакции в поддержку.
    * Админ вручную восстанавливает стрик + начисляет 3-5 "заморозок".
* **Smart Nudge:** Email отправляется через X часов после *среднего времени* активности пользователя.

---

### 5. Technical Architecture (Indie-Pro Stack)

#### 5.1. Core Stack
* **Framework:** ...
* **Styling:** Tailwind CSS (Strict typography, Monochrome).
* **State:** Zustand.
* **Animations:** Framer Motion (Zen transitions).

#### 5.2. Backend & Data
* **BaaS:** Supabase (PostgreSQL).
    * Auth: Passwordless (Magic Link via Email).
    * Database: Relational (Users, Words, Logs).
    * Edge Functions: Cron Jobs for Daily Digest.
* **AI:** OpenAI API (gpt-4o-mini for validation, gpt-4o for digest).

#### 5.3. Email Infrastructure
* **Provider:** Resend (React Email components).

### 6. Database Schema (Draft)

```sql
-- 1. Users
table users {
  id: uuid (pk)
  email: text
  timezone: text            -- Critical for morning delivery
  streak_current: int       -- North Star Metric
  last_practice_at: timestamp
  is_frozen: boolean
}

-- 2. Words
table words {
  id: uuid (pk)
  user_id: uuid (fk)
  original: text
  translation: text
  context_snippet: text     -- First usage example
  weight: float (default 1.0) -- SRS Probability
  next_review_at: timestamp
}

-- 3. Practice Logs
table practice_logs {
  id: uuid (pk)
  word_id: uuid (fk)
  user_input: text
  ai_status: enum ('green', 'green_star', 'yellow', 'red')
  ai_feedback: text
  created_at: timestamp
}
```

### 7. Success Metrics (KPIs)
North Star: Streak Integrity (% Active Users with streak > 7 days).
    Rationale: Доказывает формирование привычки и ценность продукта.
