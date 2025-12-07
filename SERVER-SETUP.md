# Инструкция по установке на сервер (с существующим nginx)

У вас уже есть nginx на сервере. Будем использовать его для hub-cargo.ru.

## 📋 План:
1. Запустить cargo БЕЗ встроенного nginx (на портах 8001 и 3001)
2. Добавить конфигурацию hub-cargo.ru в существующий nginx
3. Получить SSL сертификат через certbot

---

## 🚀 Шаг 1: Установка cargo (на сервере)

```bash
ssh root@5.35.80.213

# Проверка что Docker и Git установлены
docker --version || curl -fsSL https://get.docker.com | sh
git --version || apt install git -y
docker-compose --version || apt install docker-compose -y

# Клонирование проекта (если еще не сделано)
cd /opt
git clone https://github.com/AmRaul/cargo.git
cd cargo

# Создание .env файла
# ВАЖНО: сначала настройте GitHub Secrets (см. GITHUB-SECRETS-SETUP.md)
# или создайте .env вручную:
cp .env.production.example .env
nano .env
# Измените: POSTGRES_PASSWORD, SECRET_KEY, ADMIN_PASSWORD
```

## 🚀 Шаг 2: Запуск cargo БЕЗ nginx

```bash
cd /opt/cargo

# Использовать конфигурацию без nginx
cp docker-compose.prod-no-nginx.yml docker-compose.prod.yml

# Запуск
chmod +x deploy.sh
./deploy.sh
```

Теперь запущены:
- ✅ Backend на `localhost:8001`
- ✅ Frontend на `localhost:3001`
- ✅ PostgreSQL (внутри Docker сети)

Проверка:
```bash
curl http://localhost:8001/health
# Должно вернуть: {"status":"healthy"}

curl http://localhost:3001
# Должна вернуться HTML страница Next.js
```

## 🚀 Шаг 3: Настройка nginx

```bash
# Копирование конфигурации
cp /opt/cargo/nginx-host-config.conf /etc/nginx/sites-available/hub-cargo

# Активация сайта
ln -s /etc/nginx/sites-available/hub-cargo /etc/nginx/sites-enabled/

# Проверка конфигурации
nginx -t

# Перезагрузка nginx
systemctl reload nginx
```

## 🚀 Шаг 4: Получение SSL сертификата

```bash
# Установка certbot (если еще не установлен)
apt install certbot python3-certbot-nginx -y

# Создание директории для certbot challenge
mkdir -p /var/www/certbot

# Получение сертификата
certbot --nginx -d hub-cargo.ru -d www.hub-cargo.ru

# Следуйте инструкциям certbot:
# - Укажите email
# - Согласитесь с условиями
# - Выберите: 2 (Redirect - automatically redirect HTTP to HTTPS)
```

Certbot автоматически:
- Получит SSL сертификат
- Обновит nginx конфигурацию
- Настроит автообновление сертификата

## ✅ Проверка

После всех шагов проверьте:

```bash
# Статус контейнеров
docker ps

# Логи cargo
docker-compose -f docker-compose.prod.yml logs -f

# Статус nginx
systemctl status nginx

# Проверка сертификата
certbot certificates
```

Откройте в браузере:
- https://hub-cargo.ru - должен открыться сайт
- https://hub-cargo.ru/docs - API документация
- https://hub-cargo.ru/health - health check

## 🔄 Автообновление (GitHub Actions)

После настройки GitHub Secrets (см. GITHUB-SECRETS-SETUP.md), каждый `git push` будет автоматически:
1. Обновлять код на сервере
2. Пересобирать контейнеры
3. Перезапускать сервисы

Nginx трогать не нужно - он уже настроен!

## 📝 Полезные команды

```bash
# Перезапуск cargo
cd /opt/cargo
docker-compose -f docker-compose.prod.yml restart

# Обновление вручную
cd /opt/cargo
git pull origin main
./deploy.sh

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Перезагрузка nginx
systemctl reload nginx

# Просмотр логов nginx
tail -f /var/log/nginx/hub-cargo.access.log
tail -f /var/log/nginx/hub-cargo.error.log

# Backup базы данных
docker exec cargo_db_prod pg_dump -U cargo_user cargo_db > backup_$(date +%Y%m%d).sql
```

## 🆘 Troubleshooting

### Контейнеры не запускаются
```bash
docker-compose -f docker-compose.prod.yml logs
docker-compose -f docker-compose.prod.yml ps
```

### Nginx ошибки
```bash
nginx -t  # Проверка конфигурации
tail -f /var/log/nginx/error.log
```

### Порты заняты
```bash
# Проверить что слушает порты
lsof -i :8001
lsof -i :3001
```

### SSL не работает
```bash
certbot certificates  # Проверить статус
certbot renew --dry-run  # Тест обновления
```

## 📊 Архитектура

```
Интернет
    ↓
hub-cargo.ru:443 (HTTPS)
    ↓
Nginx (:80, :443) - существующий nginx на сервере
    ↓
    ├─→ /api/* → Backend (localhost:8001)
    ├─→ /docs → Backend (localhost:8001)
    └─→ /* → Frontend (localhost:3001)
           ↓
      Docker containers:
      - cargo_frontend_prod (Next.js)
      - cargo_backend_prod (FastAPI)
      - cargo_db_prod (PostgreSQL)
```

Готово! 🎉
