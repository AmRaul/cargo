# Cargo Logistics Accounting System - Setup Guide

Система учёта грузоперевозок с автоматическим расчётом финансовых показателей.

## Что реализовано

### 1. База данных (PostgreSQL + UUID)
- **Suppliers** - Поставщики/Origin (откуда груз)
- **Clients** - Клиенты
- **Rates** - Ставки закупки и продажи
- **Shipments** - Поставки/Фуры (с уникальным shipment_code)
- **Expenses** - Расходы по поставке

### 2. Автоматические финансовые расчёты
- **Revenue** (выручка) = quantity × sell_rate
- **Cost of Goods** (себестоимость) = quantity × buy_rate
- **Total Expenses** = SUM(expenses.amount)
- **Profit** (прибыль) = revenue - cost - expenses
- **Margin %** = (profit / revenue) × 100

### 3. Backend API (FastAPI)
- CRUD endpoints для всех сущностей
- Финансовые отчёты (по периоду, по клиенту, по поставщику)
- Endpoint для расчёта финансов: `GET /api/v1/shipments/{id}/finance`

### 4. Admin Panel (SQLAdmin)
- Удобная админка на `/admin`
- Аутентификация: username=`admin`, password из `.env` (`ADMIN_PASSWORD`)
- Управление всеми сущностями через веб-интерфейс

### 5. Alembic Migrations
- Система миграций для управления изменениями БД
- Initial migration уже создана

---

## Быстрый старт

### 1. Установка зависимостей

```bash
cd backend
pip install -r requirements.txt
```

### 2. Настройка .env

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql://cargo_user:cargo_pass@localhost:5432/cargo_db
SECRET_KEY=your-super-secret-key-change-this
ADMIN_PASSWORD=your-admin-password
```

### 3. Запуск PostgreSQL

Если используете Docker:

```bash
docker run --name cargo-postgres \
  -e POSTGRES_USER=cargo_user \
  -e POSTGRES_PASSWORD=cargo_pass \
  -e POSTGRES_DB=cargo_db \
  -p 5432:5432 \
  -d postgres:15
```

### 4. Применение миграций

```bash
cd backend
alembic upgrade head
```

### 5. Создание тестовых данных (опционально)

```bash
cd backend
python create_initial_data.py
```

Это создаст:
- 2 поставщика (Shanghai Trading Co, Guangzhou Logistics)
- 2 клиента (Petrov Trading, Sidorova Import)
- 3 ставки
- 3 поставки
- 4 расхода

### 6. Запуск сервера

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Использование

### Admin Panel

1. Откройте браузер: http://localhost:8000/admin
2. Войдите с данными:
   - Username: `admin`
   - Password: ваш `ADMIN_PASSWORD` из `.env`

3. Доступные разделы:
   - **Suppliers** - управление поставщиками
   - **Clients** - управление клиентами
   - **Rates** - управление ставками
   - **Shipments** - управление поставками
   - **Expenses** - управление расходами

### API Endpoints

**API Documentation:** http://localhost:8000/docs

#### Справочники:
- `POST /api/v1/suppliers` - создать поставщика
- `GET /api/v1/suppliers` - список поставщиков
- `GET /api/v1/suppliers/{id}` - получить поставщика
- `PATCH /api/v1/suppliers/{id}` - обновить поставщика
- `DELETE /api/v1/suppliers/{id}` - удалить поставщика

Аналогично для `/clients` и `/rates`

#### Поставки:
- `POST /api/v1/shipments` - создать поставку
- `GET /api/v1/shipments` - список поставок
- `GET /api/v1/shipments/{id}` - получить поставку
- `GET /api/v1/shipments/{id}/finance` - **получить поставку с финансами**
- `PATCH /api/v1/shipments/{id}` - обновить поставку
- `DELETE /api/v1/shipments/{id}` - удалить поставку

#### Расходы:
- `POST /api/v1/expenses` - создать расход
- `GET /api/v1/expenses?shipment_id={id}` - список расходов (можно фильтровать)
- `GET /api/v1/expenses/{id}` - получить расход
- `PATCH /api/v1/expenses/{id}` - обновить расход
- `DELETE /api/v1/expenses/{id}` - удалить расход

#### Отчёты:
- `GET /api/v1/reports/summary?date_from=2024-01-01&date_to=2024-12-31` - сводный отчёт
- `GET /api/v1/reports/by-client/{client_id}` - отчёт по клиенту
- `GET /api/v1/reports/by-supplier/{supplier_id}` - отчёт по поставщику

---

## Примеры использования API

### Создать поставку

```bash
curl -X POST http://localhost:8000/api/v1/shipments \
  -H "Content-Type: application/json" \
  -d '{
    "shipment_code": "CN-RU-004",
    "supplier_id": "uuid-here",
    "client_id": "uuid-here",
    "rate_id": "uuid-here",
    "cargo_type": "perfumes",
    "quantity": 1000,
    "departure_date": "2024-12-01",
    "status": "planned"
  }'
```

### Получить поставку с финансами

```bash
curl http://localhost:8000/api/v1/shipments/{shipment_id}/finance
```

Ответ:
```json
{
  "id": "...",
  "shipment_code": "CN-RU-001",
  "cargo_type": "perfumes",
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

---

## Структура проекта

```
backend/
├── app/
│   ├── models/          # SQLAlchemy модели
│   │   ├── supplier.py
│   │   ├── client.py
│   │   ├── rate.py
│   │   ├── shipment.py
│   │   └── expense.py
│   ├── schemas/         # Pydantic схемы
│   │   ├── supplier.py
│   │   ├── client.py
│   │   ├── rate.py
│   │   ├── shipment.py
│   │   └── expense.py
│   ├── api/             # API endpoints
│   │   ├── suppliers.py
│   │   ├── clients.py
│   │   ├── rates.py
│   │   ├── shipments.py
│   │   ├── expenses.py
│   │   └── reports.py
│   ├── admin/           # SQLAdmin views
│   │   └── views.py
│   ├── services/        # Бизнес-логика
│   │   └── finance.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   └── main.py
├── alembic/             # Миграции БД
│   ├── versions/
│   └── env.py
├── alembic.ini
├── requirements.txt
└── create_initial_data.py
```

---

## Миграции БД

### Создать новую миграцию

```bash
cd backend
alembic revision --autogenerate -m "описание изменений"
```

### Применить миграции

```bash
alembic upgrade head
```

### Откатить последнюю миграцию

```bash
alembic downgrade -1
```

---

## Следующие шаги (TODO)

1. ✅ Базовая структура БД
2. ✅ CRUD API для всех сущностей
3. ✅ Финансовые расчёты
4. ✅ SQLAdmin панель
5. ✅ Отчёты
6. 🔲 Добавить computed columns в SQLAdmin для отображения финансов
7. 🔲 Добавить валидацию дат (departure_date < arrival_date)
8. 🔲 Добавить пагинацию в отчётах
9. 🔲 Экспорт отчётов в Excel/CSV
10. 🔲 Dashboard с графиками

---

## Troubleshooting

### Ошибка подключения к БД

Проверьте что PostgreSQL запущен и `DATABASE_URL` в `.env` корректный.

### Ошибка при миграции

Убедитесь что БД создана и доступна:

```bash
psql -U cargo_user -d cargo_db -h localhost
```

### SQLAdmin не показывает данные

Убедитесь что миграции применены:

```bash
alembic current  # Показывает текущую версию
alembic upgrade head  # Применяет все миграции
```

---

## Контакты

Для вопросов и предложений создавайте issue в репозитории.
