# 🚚 Cargo Logistics Accounting System

Система учёта грузоперевозок с автоматическим расчётом финансовых показателей (revenue, cost, profit, margin).

## 🎯 Возможности

- ✅ **Учёт поставщиков и клиентов** - полная база контрагентов
- ✅ **Гибкие ставки** - закупка/продажа по разным тарифам
- ✅ **Управление поставками** - отслеживание статусов фур
- ✅ **Учёт расходов** - таможня, доставка, склад, агентские
- ✅ **Автоматические финансы** - revenue, cost, profit, margin
- ✅ **Отчётность** - по периодам, клиентам, поставщикам
- ✅ **Admin Panel** - удобный веб-интерфейс
- ✅ **REST API** - полный CRUD для интеграций

## 🚀 Быстрый старт (Docker)

### Вариант 1: Автоматический (рекомендуется)

```bash
./START.sh
```

Скрипт автоматически:
- ✅ Создаст `.env` из `.env.example` если его нет
- ✅ Запустит контейнеры
- ✅ Применит миграции БД
- ✅ Создаст тестовые данные

### Вариант 2: Ручной

```bash
# 1. Создать .env файл
cp .env.example .env

# 2. (Опционально) Изменить пароли в .env
nano .env  # или любой другой редактор

# 3. Запустить всё
docker-compose up --build -d

# 4. Создать тестовые данные
docker-compose exec backend python create_initial_data.py
```

### 🔐 Доступ к админке

- **URL**: http://localhost:8000/admin
- **Username**: `admin`
- **Password**: Смотри в `.env` файле (по умолчанию `admin123`)

**Готово!** 🎉

## 📚 Документация

- [**DOCKER-QUICKSTART.md**](DOCKER-QUICKSTART.md) - Полная инструкция по Docker
- [**CARGO-LOGISTICS-SETUP.md**](CARGO-LOGISTICS-SETUP.md) - Техническая документация API

## 🌐 Доступные URL

После запуска:

| Сервис | URL | Описание |
|--------|-----|----------|
| Admin Panel | http://localhost:8000/admin | Веб-интерфейс управления |
| API Docs | http://localhost:8000/docs | Swagger документация |
| API | http://localhost:8000/api/v1 | REST API endpoints |

## 📊 Структура данных

### База данных (PostgreSQL + UUID)

```
Suppliers (поставщики)
  ↓
Rates (ставки: buy_rate / sell_rate)
  ↓
Shipments (поставки) ← финансовые расчёты
  ↓
Expenses (расходы)
  ↓
Clients (клиенты)
```

### Финансовые формулы

```
Revenue = quantity × sell_rate
Cost of Goods = quantity × buy_rate
Total Expenses = SUM(expenses)
Profit = revenue - cost - expenses
Margin % = (profit / revenue) × 100
```

## 🔌 Основные API endpoints

```bash
# Suppliers
GET    /api/v1/suppliers
POST   /api/v1/suppliers
PATCH  /api/v1/suppliers/{id}
DELETE /api/v1/suppliers/{id}

# Clients
GET    /api/v1/clients
POST   /api/v1/clients
...

# Rates
GET    /api/v1/rates
POST   /api/v1/rates
...

# Shipments (с финансами!)
GET    /api/v1/shipments
POST   /api/v1/shipments
GET    /api/v1/shipments/{id}/finance  # 💰 С расчётом финансов
PATCH  /api/v1/shipments/{id}
DELETE /api/v1/shipments/{id}

# Expenses
GET    /api/v1/expenses?shipment_id={id}
POST   /api/v1/expenses
...

# Reports
GET    /api/v1/reports/summary?date_from=...&date_to=...
GET    /api/v1/reports/by-client/{client_id}
GET    /api/v1/reports/by-supplier/{supplier_id}
```

## 💡 Примеры использования

### Создать поставку

```bash
curl -X POST http://localhost:8000/api/v1/shipments \
  -H "Content-Type: application/json" \
  -d '{
    "shipment_code": "CN-RU-004",
    "supplier_id": "...",
    "client_id": "...",
    "rate_id": "...",
    "cargo_type": "perfumes",
    "quantity": 1000,
    "status": "planned"
  }'
```

### Получить финансы по поставке

```bash
curl http://localhost:8000/api/v1/shipments/{id}/finance
```

Ответ:
```json
{
  "shipment_code": "CN-RU-001",
  "quantity": 500,
  "revenue": 1050.00,
  "cost_of_goods": 890.00,
  "total_expenses": 230.00,
  "profit": -70.00,
  "margin_percent": -6.67
}
```

### Получить сводный отчёт

```bash
curl "http://localhost:8000/api/v1/reports/summary?date_from=2024-01-01&date_to=2024-12-31"
```

## 🛠 Технологии

- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic
- **Database**: PostgreSQL 15 (UUID)
- **Admin**: SQLAdmin
- **Container**: Docker, Docker Compose
- **Python**: 3.11

## 📁 Структура проекта

```
cargo/
├── docker-compose.yml              # Docker конфигурация
├── DOCKER-QUICKSTART.md           # Инструкция Docker
├── CARGO-LOGISTICS-SETUP.md       # Техническая документация
├── README.md                      # Этот файл
└── backend/
    ├── Dockerfile                 # Образ backend
    ├── entrypoint.sh             # Автозапуск миграций
    ├── requirements.txt          # Python зависимости
    ├── alembic/                  # Миграции БД
    ├── app/
    │   ├── main.py              # FastAPI приложение
    │   ├── models/              # SQLAlchemy модели
    │   ├── schemas/             # Pydantic схемы
    │   ├── api/                 # API endpoints
    │   ├── admin/               # SQLAdmin views
    │   ├── services/            # Бизнес-логика
    │   └── core/                # Config, Database
    └── create_initial_data.py   # Тестовые данные
```

## 🔧 Команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Логи
docker-compose logs -f backend

# Применить миграции
docker-compose exec backend alembic upgrade head

# Создать тестовые данные
docker-compose exec backend python create_initial_data.py

# Подключиться к БД
docker-compose exec postgres psql -U cargo_user -d cargo_db
```

## 🔐 Безопасность

⚠️ **ВАЖНО**: Перед деплоем на production:

1. **Создайте `.env` файл** (не коммитьте в git!):
   ```bash
   cp .env.example .env
   ```

2. **Измените пароли в `.env`**:
   ```env
   ADMIN_PASSWORD=ваш-сложный-пароль
   SECRET_KEY=ваш-секретный-ключ-32-символа
   POSTGRES_PASSWORD=пароль-для-бд
   ```

3. **Сгенерируйте безопасный SECRET_KEY**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

4. **Никогда не коммитьте `.env` в git!** (уже в `.gitignore`)

## 📝 Разработка

### Создание новой миграции

```bash
docker-compose exec backend alembic revision --autogenerate -m "описание"
docker-compose exec backend alembic upgrade head
```

### Откат миграции

```bash
docker-compose exec backend alembic downgrade -1
```

## 🐛 Troubleshooting

### Контейнер не запускается

```bash
docker-compose logs backend
docker-compose down
docker-compose up --build
```

### Нужно очистить БД

```bash
docker-compose down -v
docker-compose up --build -d
docker-compose exec backend python create_initial_data.py
```

Подробнее см. [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md)

## 📄 Лицензия

MIT

## 👨‍💻 Автор

Cargo Logistics Team
