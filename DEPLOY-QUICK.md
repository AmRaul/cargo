# Быстрое развертывание на сервере

## 🚀 Краткая инструкция

### Вариант 1: Автоматический деплой через GitHub (Рекомендуется)

**См. подробную инструкцию**: [GITHUB-SECRETS-SETUP.md](GITHUB-SECRETS-SETUP.md)

**Кратко:**
1. Сгенерируйте пароли локально
2. Добавьте 6 секретов в GitHub
3. Сделайте `git push` - деплой произойдет автоматически!

---

### Вариант 2: Ручной деплой на сервере

```bash
# 1. Подключение
ssh root@5.35.80.213

# 2. Установка Docker и Git
curl -fsSL https://get.docker.com | sh
apt install docker-compose git -y

# 3. Клонирование проекта
cd /opt
git clone https://github.com/AmRaul/cargo.git
cd cargo

# 4. Настройка переменных окружения
cp .env.production.example .env
nano .env
# Измените: POSTGRES_PASSWORD, SECRET_KEY, ADMIN_PASSWORD
# Используйте: openssl rand -hex 32 и openssl rand -base64 24

# 5. Настройка SSL
nano init-ssl.sh  # Измените EMAIL
chmod +x init-ssl.sh
./init-ssl.sh

# 6. Запуск
chmod +x deploy.sh
./deploy.sh
```

### Настройка GitHub Actions (для автодеплоя)

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
