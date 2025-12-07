# ✅ Cargo успешно задеплоен на сервере!

Backend и Frontend работают на портах **8001** и **3001**.

## 🎯 Осталось сделать 2 шага:

### Шаг 1: Проверить что всё работает

На сервере выполните:

```bash
# Проверка backend
curl http://localhost:8001/health
# Должно вернуть: {"status":"healthy"}

# Проверка frontend
curl http://localhost:3001
# Должна вернуться HTML страница

# Проверка логов
docker ps
docker-compose -f docker-compose.prod.yml logs -f
```

### Шаг 2: Настроить существующий nginx

```bash
# 1. Скопировать конфигурацию
cp /opt/cargo/nginx-host-config.conf /etc/nginx/sites-available/hub-cargo

# 2. Активировать сайт
ln -s /etc/nginx/sites-available/hub-cargo /etc/nginx/sites-enabled/

# 3. Проверить конфигурацию
nginx -t

# 4. Если проверка OK - перезагрузить nginx
systemctl reload nginx

# 5. Получить SSL сертификат
apt install certbot python3-certbot-nginx -y
mkdir -p /var/www/certbot
certbot --nginx -d hub-cargo.ru -d www.hub-cargo.ru
```

### Шаг 3: Проверить сайт

Откройте в браузере:
- http://hub-cargo.ru → должен перенаправить на HTTPS
- https://hub-cargo.ru → главная страница сайта
- https://hub-cargo.ru/docs → API документация
- https://hub-cargo.ru/health → `{"status":"healthy"}`

## 🔄 Автодеплой уже работает!

Теперь при каждом `git push origin main`:
1. GitHub Actions автоматически обновит код на сервере
2. Пересоберет контейнеры
3. Перезапустит сервисы

Nginx трогать не нужно - он уже настроен!

## 📝 Полезные команды

```bash
# Просмотр логов cargo
cd /opt/cargo
docker-compose -f docker-compose.prod.yml logs -f

# Просмотр логов nginx
tail -f /var/log/nginx/hub-cargo.access.log
tail -f /var/log/nginx/hub-cargo.error.log

# Перезапуск cargo
docker-compose -f docker-compose.prod.yml restart

# Обновление вручную
git pull origin main
./deploy.sh
```

## 🎉 Готово!

После настройки nginx сайт будет доступен по адресу: **https://hub-cargo.ru**
