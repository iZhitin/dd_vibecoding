# DD (Daily Dict)

Minimalist Progressive Web App for language learning.

## Настройка DNS для аутентификации Email и SSL

Для корректной работы PWA с HTTPS и успешной доставки писем необходимо настроить DNS-записи для вашего домена (например, `yourdomain.com`).

### 1. A-запись (для HTTPS / Web)
Направьте домен на IP-адрес вашего сервера:
- **Type:** `A`
- **Name:** `@` (или ваш поддомен)
- **Value:** `IP_АДРЕС_СЕРВЕРА`

### 2. DKIM, SPF, DMARC (для Email / Resend)
Чтобы ваши письма не попадали в спам, настройте аутентификацию домена в сервисе рассылок (Resend). Скопируйте значения из панели Resend (раздел Domains).

Пример типичных записей (точные значения даст Resend):
- **SPF:**
  - **Type:** `TXT`
  - **Name:** `bounces`
  - **Value:** `v=spf1 include:amazonses.com ~all`
- **DKIM:**
  - **Type:** `TXT`
  - **Name:** `resend._domainkey`
  - **Value:** `p=MIGfMA0GCS...`
- **DMARC:**
  - **Type:** `TXT`
  - **Name:** `_dmarc`
  - **Value:** `v=DMARC1; p=none;`

## Получение SSL-сертификатов (первый запуск)

1. Отредактируйте `nginx/nginx.conf` и замените `yourdomain.com` на ваш реальный домен.
2. Поднимите все контейнеры (Nginx может завершаться ошибкой без сертификатов, это нормально для первого шага):
   ```bash
   docker compose up -d
   ```
3. Выполните команду для выпуска сертификата через certbot:
   ```bash
   docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d yourdomain.com -d www.yourdomain.com
   ```
4. Перезапустите Nginx:
   ```bash
   docker compose restart nginx
   ```
В дальнейшем сертификаты будут обновляться автоматически.
## База данных и миграции

Миграции запускаются автоматически при старте контейнера `backend`. Если вам нужно запустить их вручную (например, для отладки), используйте команду:

```bash
docker compose exec backend alembic upgrade head
```

## Развертывание на голом IP (без домена)

Если вы запускаете проект на VPS без привязанного домена:

1. В `.env` установите `APP_URL=http://ВАШ_IP`.
2. В `nginx/nginx.conf` установите `server_name ВАШ_IP`.
3. Убедитесь, что SSL параметры в `nginx/nginx.conf` закомментированы или удалены, так как SSL (Certbot) не работает для IP-адресов.
4. В `backend/.env` убедитесь, что `DATABASE_URL` и `REDIS_URL` указывают на имена сервисов (`db` и `redis`), а не на `localhost`.

## Полезные команды

- Просмотр логов: `docker compose logs -f backend`
- Перезапуск сервисов с пересборкой: `docker compose up -d --build`
- Очистка неиспользуемых ресурсов Docker (если закончилось место): `docker system prune -a`
