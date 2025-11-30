# Инструкция по развертыванию на сервере

## Информация о сервере
- **Домен**: hub-cargo.ru
- **IP**: 5.35.80.213
- **Репозиторий**: https://github.com/AmRaul/cargo.git

## 1. Подготовка сервера

### Подключение к серверу
```bash
ssh root@5.35.80.213
```

### Установка необходимого ПО
```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
apt install docker-compose -y

# Установка Git
apt install git -y
```

## 2. Настройка DNS

Убедитесь, что в DNS записях вашего домена настроены A-записи:
```
A    hub-cargo.ru      -> 5.35.80.213
A    www.hub-cargo.ru  -> 5.35.80.213
```

## 3. Клонирование репозитория

```bash
# Создание директории для проекта
mkdir -p /opt/cargo
cd /opt/cargo

# Клонирование репозитория
git clone https://github.com/AmRaul/cargo.git .
```

## 4. Настройка переменных окружения

```bash
# Копирование шаблона
cp .env.production.example .env

# Редактирование .env файла
nano .env
```

**Важно!** Измените следующие значения:
- `POSTGRES_PASSWORD` - надежный пароль для базы данных
- `SECRET_KEY` - случайный ключ (можно сгенерировать: `openssl rand -hex 32`)
- `ADMIN_PASSWORD` - пароль для админ-панели

Пример `.env`:
```env
POSTGRES_USER=cargo_user
POSTGRES_PASSWORD=MyStr0ngP@ssw0rd123!
POSTGRES_DB=cargo_db

DATABASE_URL=postgresql://cargo_user:MyStr0ngP@ssw0rd123!@postgres:5432/cargo_db
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
ADMIN_PASSWORD=Admin123!Secure

NEXT_PUBLIC_API_URL=https://hub-cargo.ru/api

ENVIRONMENT=production
```

## 5. Настройка SSL сертификатов

```bash
# Редактируем email в скрипте
nano init-ssl.sh
# Измените EMAIL="your-email@example.com" на ваш реальный email

# Запуск скрипта инициализации SSL
./init-ssl.sh
```

Этот скрипт автоматически:
- Получит SSL сертификаты от Let's Encrypt
- Настроит автообновление сертификатов
- Включит HTTPS для вашего домена

## 6. Первый запуск

```bash
# Запуск всех сервисов
./deploy.sh
```

Скрипт автоматически:
- Соберет Docker образы
- Запустит контейнеры
- Проверит статус сервисов

## 7. Проверка работоспособности

После успешного запуска проверьте:

- **Frontend**: https://hub-cargo.ru
- **API Docs**: https://hub-cargo.ru/docs
- **Health Check**: https://hub-cargo.ru/health

```bash
# Проверка логов
docker-compose -f docker-compose.prod.yml logs -f

# Проверка статуса контейнеров
docker-compose -f docker-compose.prod.yml ps

# Проверка конкретного сервиса
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
docker-compose -f docker-compose.prod.yml logs nginx
```

## 8. Настройка GitHub Actions для автодеплоя

### Генерация SSH ключа
```bash
# На вашем локальном компьютере или на сервере
ssh-keygen -t ed25519 -C "github-actions-cargo" -f ~/.ssh/github_cargo

# Копирование публичного ключа на сервер
ssh-copy-id -i ~/.ssh/github_cargo.pub root@5.35.80.213

# Показать приватный ключ (скопируйте его)
cat ~/.ssh/github_cargo
```

### Добавление секретов в GitHub

Перейдите в Settings → Secrets and variables → Actions вашего репозитория:

1. **SERVER_HOST**: `5.35.80.213`
2. **SERVER_USER**: `root`
3. **SSH_PRIVATE_KEY**: содержимое файла `~/.ssh/github_cargo` (приватный ключ)

### Тестирование автодеплоя

После настройки секретов:
```bash
# Сделайте любое изменение и запушьте в main
git add .
git commit -m "Test auto-deploy"
git push origin main
```

GitHub Actions автоматически:
- Подключится к серверу
- Выполнит `git pull`
- Запустит `deploy.sh`

## 9. Управление проектом

### Обновление вручную
```bash
cd /opt/cargo
git pull origin main
./deploy.sh
```

### Просмотр логов
```bash
# Все логи
docker-compose -f docker-compose.prod.yml logs -f

# Только backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Только frontend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100 -f
```

### Перезапуск сервисов
```bash
# Все сервисы
docker-compose -f docker-compose.prod.yml restart

# Только backend
docker-compose -f docker-compose.prod.yml restart backend

# Только frontend
docker-compose -f docker-compose.prod.yml restart frontend
```

### Остановка проекта
```bash
docker-compose -f docker-compose.prod.yml down
```

### Полная очистка (включая данные БД!)
```bash
docker-compose -f docker-compose.prod.yml down -v
```

## 10. Резервное копирование базы данных

### Создание backup
```bash
# Создать директорию для бэкапов
mkdir -p /opt/cargo/backups

# Создать backup
docker exec cargo_db_prod pg_dump -U cargo_user cargo_db > /opt/cargo/backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

### Восстановление из backup
```bash
# Восстановить из конкретного файла
docker exec -i cargo_db_prod psql -U cargo_user cargo_db < /opt/cargo/backups/backup_20241130_150000.sql
```

### Автоматическое резервное копирование (cron)
```bash
# Редактирование crontab
crontab -e

# Добавить строку для ежедневного бэкапа в 3:00
0 3 * * * docker exec cargo_db_prod pg_dump -U cargo_user cargo_db > /opt/cargo/backups/backup_$(date +\%Y\%m\%d_\%H\%M\%S).sql

# Удаление старых бэкапов (старше 30 дней)
0 4 * * * find /opt/cargo/backups -name "backup_*.sql" -mtime +30 -delete
```

## 11. Мониторинг

### Проверка использования ресурсов
```bash
# Использование CPU и памяти контейнерами
docker stats

# Использование диска
df -h

# Размер образов Docker
docker system df
```

### Очистка неиспользуемых ресурсов
```bash
# Удаление неиспользуемых образов и контейнеров
docker system prune -a -f

# Удаление только образов
docker image prune -a -f
```

## 12. Troubleshooting

### Контейнер не запускается
```bash
# Проверить логи
docker-compose -f docker-compose.prod.yml logs [service_name]

# Проверить конфигурацию
docker-compose -f docker-compose.prod.yml config

# Пересоздать контейнер
docker-compose -f docker-compose.prod.yml up -d --force-recreate [service_name]
```

### Проблемы с SSL
```bash
# Проверить сертификаты
docker-compose -f docker-compose.prod.yml run --rm certbot certificates

# Обновить сертификаты вручную
docker-compose -f docker-compose.prod.yml run --rm certbot renew

# Переполучить сертификаты
./init-ssl.sh
```

### База данных не доступна
```bash
# Проверить статус PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U cargo_user

# Подключиться к БД напрямую
docker-compose -f docker-compose.prod.yml exec postgres psql -U cargo_user -d cargo_db
```

### Nginx не работает
```bash
# Проверить конфигурацию nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Перезагрузить nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

## 13. Безопасность

### Настройка firewall (ufw)
```bash
# Установка ufw
apt install ufw -y

# Разрешить SSH
ufw allow 22/tcp

# Разрешить HTTP и HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Включить firewall
ufw enable

# Проверить статус
ufw status
```

### Обновление зависимостей
```bash
# Обновление Docker образов
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Обновление системы
apt update && apt upgrade -y
```

## 14. Порты и конфликты

Проект использует следующие порты:
- **80** - HTTP (Nginx) - перенаправление на HTTPS
- **443** - HTTPS (Nginx) - основной трафик
- **Внутренние порты** (только в Docker сети):
  - 5432 - PostgreSQL
  - 8000 - Backend (FastAPI)
  - 3000 - Frontend (Next.js)

Если на сервере уже запущены другие проекты (VPN, backtester), конфликтов не будет, так как:
- Nginx работает на стандартных портах 80/443
- Внутренние сервисы изолированы в Docker сети `cargo_network_prod`
- Каждый контейнер имеет уникальное имя

## Контакты и поддержка

При возникновении проблем проверьте:
1. Логи сервисов
2. Статус контейнеров
3. Доступность портов
4. DNS записи
5. SSL сертификаты

Удачного развертывания! 🚀
