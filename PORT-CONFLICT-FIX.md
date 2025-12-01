# Решение конфликта портов 80/443

## Проблема
На сервере уже работает другой сервис (nginx/apache) или Docker контейнер, использующий порты 80 и 443.

## 🔍 Диагностика

На сервере выполните:
```bash
# Проверить что использует порт 80
sudo lsof -i :80
# или
docker ps --filter "publish=80"

# Проверить что использует порт 443
sudo lsof -i :443
# или
docker ps --filter "publish=443"
```

## ✅ Решение 1: Использовать существующий Nginx (Рекомендуется)

Если у вас уже есть Nginx для других проектов (VPN, backtester), добавьте конфигурацию cargo в него:

### 1. Запустите cargo БЕЗ встроенного nginx:

```bash
# На сервере
cd /opt/cargo
cp docker-compose.prod-no-nginx.yml docker-compose.prod.yml
./deploy.sh
```

Это запустит:
- Backend на порту **8001** (вместо внутреннего 8000)
- Frontend на порту **3001** (вместо внутреннего 3000)

### 2. Добавьте конфигурацию в существующий Nginx:

Скопируйте содержимое `nginx/conf.d/cargo.conf` в ваш существующий nginx:

```bash
# Если используется nginx вне Docker
sudo cp /opt/cargo/nginx/conf.d/cargo.conf /etc/nginx/sites-available/cargo
sudo ln -s /etc/nginx/sites-available/cargo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Если используется nginx в Docker
# Добавьте volume с конфигурацией в ваш nginx контейнер
```

### 3. Измените upstream в конфигурации:

Отредактируйте конфигурацию nginx, измените upstream:

```nginx
upstream backend {
    server localhost:8001;  # Изменено с cargo_backend_prod:8000
}

upstream frontend {
    server localhost:3001;  # Изменено с cargo_frontend_prod:3000
}
```

## ✅ Решение 2: Остановить конфликтующие контейнеры

Если порты заняты временно или ненужными контейнерами:

```bash
# Найти контейнеры на портах 80/443
docker ps --filter "publish=80"
docker ps --filter "publish=443"

# Остановить их
docker stop <container_id>

# Или остановить все nginx контейнеры
docker stop $(docker ps -q -f name=nginx)

# Запустить cargo деплой
cd /opt/cargo
./deploy.sh
```

## ✅ Решение 3: Использовать другие порты для Cargo

Измените `docker-compose.prod.yml`:

```yaml
nginx:
  # ...
  ports:
    - "8080:80"    # HTTP на 8080 вместо 80
    - "8443:443"   # HTTPS на 8443 вместо 443
```

Затем обновите настройку DNS/firewall для перенаправления:
- hub-cargo.ru:80 → сервер:8080
- hub-cargo.ru:443 → сервер:8443

## ✅ Решение 4: Автоматическое освобождение портов (Агрессивное)

⚠️ **Внимание**: Это остановит ВСЕ контейнеры на портах 80/443!

Обновленный `deploy.sh` уже содержит эту логику. При деплое будут остановлены все контейнеры, использующие порты 80/443.

## 🎯 Рекомендация для вашего случая

Поскольку на сервере уже работают VPN и backtester, **используйте Решение 1**:

1. Используйте `docker-compose.prod-no-nginx.yml`
2. Настройте существующий nginx как reverse proxy для портов 8001 (backend) и 3001 (frontend)
3. Все проекты будут использовать один nginx - без конфликтов

### Быстрая настройка:

```bash
ssh root@5.35.80.213

# 1. Проверить текущий nginx
docker ps | grep nginx

# 2. Переключить cargo на no-nginx режим
cd /opt/cargo
cp docker-compose.prod-no-nginx.yml docker-compose.prod.yml

# 3. Обновить .env для корректного API URL
echo "NEXT_PUBLIC_API_URL=https://hub-cargo.ru/api" >> .env

# 4. Деплой
./deploy.sh

# 5. Настроить существующий nginx (если нужно)
# Добавьте proxy_pass в конфигурацию существующего nginx
```

## 📝 Конфигурация для существующего Nginx

Добавьте в ваш существующий nginx config:

```nginx
# /etc/nginx/sites-available/cargo или в вашем nginx контейнере

server {
    listen 80;
    server_name hub-cargo.ru www.hub-cargo.ru;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name hub-cargo.ru www.hub-cargo.ru;

    ssl_certificate /etc/letsencrypt/live/hub-cargo.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hub-cargo.ru/privkey.pem;

    # API
    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~ ^/(docs|redoc|openapi.json|health) {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
    }

    # Frontend
    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🆘 Проверка после изменений

```bash
# Проверить запущенные контейнеры
docker ps

# Проверить порты
netstat -tlnp | grep -E ":(80|443|8001|3001)"

# Проверить логи
docker-compose -f docker-compose.prod.yml logs -f

# Тест доступности
curl http://localhost:8001/health  # Backend
curl http://localhost:3001         # Frontend
```
