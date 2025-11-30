# Быстрое развертывание на сервере

## 🚀 Краткая инструкция

### На сервере (5.35.80.213)

```bash
# 1. Подключение
ssh root@5.35.80.213

# 2. Установка Docker и Git (если еще не установлены)
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
apt install docker-compose git -y

# 3. Клонирование проекта
mkdir -p /opt/cargo && cd /opt/cargo
git clone https://github.com/AmRaul/cargo.git .

# 4. Настройка переменных окружения
cp .env.production.example .env
nano .env
# Измените: POSTGRES_PASSWORD, SECRET_KEY, ADMIN_PASSWORD

# 5. Настройка SSL
nano init-ssl.sh
# Измените EMAIL на ваш email
./init-ssl.sh

# 6. Запуск
./deploy.sh
```

### Настройка GitHub Actions (автодеплой)

```bash
# На локальном компьютере или сервере
ssh-keygen -t ed25519 -C "github-cargo" -f ~/.ssh/github_cargo
ssh-copy-id -i ~/.ssh/github_cargo.pub root@5.35.80.213
cat ~/.ssh/github_cargo  # Скопируйте приватный ключ
```

Добавьте в GitHub (Settings → Secrets → Actions):
- `SERVER_HOST`: `5.35.80.213`
- `SERVER_USER`: `root`
- `SSH_PRIVATE_KEY`: приватный ключ из команды выше

### Проверка

После деплоя:
- Frontend: https://hub-cargo.ru
- API: https://hub-cargo.ru/docs
- Health: https://hub-cargo.ru/health

### Полезные команды

```bash
# Логи
docker-compose -f docker-compose.prod.yml logs -f

# Статус
docker-compose -f docker-compose.prod.yml ps

# Перезапуск
docker-compose -f docker-compose.prod.yml restart

# Обновление
cd /opt/cargo && git pull && ./deploy.sh

# Backup БД
docker exec cargo_db_prod pg_dump -U cargo_user cargo_db > backup_$(date +%Y%m%d).sql
```

📖 **Подробная инструкция**: см. [DEPLOYMENT.md](DEPLOYMENT.md)
