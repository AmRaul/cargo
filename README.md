# Cargo Express - Платформа для грузоперевозок

Лендинг для приема заявок на грузоперевозки из ОАЭ и Турции в РФ.

## Стек технологий

### Frontend
- **Next.js 14** - React фреймворк
- **TypeScript** - типизация
- **Tailwind CSS** - стили
- **Framer Motion** - анимации
- **React Hook Form** - формы
- **Axios** - HTTP клиент

### Backend
- **FastAPI** - Python веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - база данных
- **Pydantic** - валидация данных
- **FastAPI Admin** - админ панель

### Инфраструктура
- **Docker & Docker Compose** - контейнеризация
- **Nginx** (опционально) - reverse proxy

## Быстрый старт

### Предварительные требования
- Docker и Docker Compose
- Git

### Установка и запуск

1. **Клонируйте репозиторий**
```bash
git clone <repository-url>
cd cargo
```

2. **Создайте .env файл для backend**
```bash
# backend/.env
DATABASE_URL=postgresql://cargo_user:cargo_pass@postgres:5432/cargo_db
SECRET_KEY=your-secret-key-change-in-production
```

3. **Запустите все сервисы**
```bash
docker-compose up --build
```

Сервисы будут доступны по адресам:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:8000/admin (пока в разработке)

### Первый запуск

При первом запуске:
1. База данных PostgreSQL автоматически создаст необходимые таблицы
2. Frontend будет доступен сразу после сборки

## Структура проекта

```
cargo/
├── backend/                 # FastAPI приложение
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Конфигурация и база данных
│   │   ├── models/         # SQLAlchemy модели
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── admin/          # Админ панель
│   │   └── main.py         # Точка входа
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/               # Next.js приложение
│   ├── components/         # React компоненты
│   ├── pages/             # Страницы Next.js
│   ├── styles/            # Глобальные стили
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
│
└── docker-compose.yml     # Оркестрация Docker
```

## API Endpoints

### Orders (Заявки)
- `POST /api/v1/orders/` - Создать заявку
- `GET /api/v1/orders/` - Получить список заявок
- `GET /api/v1/orders/{id}` - Получить заявку по ID
- `PATCH /api/v1/orders/{id}` - Обновить заявку
- `DELETE /api/v1/orders/{id}` - Удалить заявку

### Документация
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
- `GET /openapi.json` - OpenAPI схема

## Модель данных

### Order (Заявка)
```json
{
  "client_name": "Иван Иванов",
  "client_phone": "+79991234567",
  "client_email": "email@example.com",
  "company_name": "ООО Компания",
  "route": "uae_to_rf",
  "cargo_type": "Электроника",
  "cargo_weight": 100.5,
  "cargo_volume": 1.5,
  "description": "Описание груза",
  "pickup_address": "Дубай, улица...",
  "delivery_address": "Москва, улица...",
  "status": "new",
  "estimated_price": 50000.00,
  "notes": "Примечания менеджера"
}
```

### Маршруты (Routes)
- `uae_to_rf` - ОАЭ → Россия
- `turkey_to_rf` - Турция → Россия

### Статусы (Status)
- `new` - Новая заявка
- `in_progress` - В работе
- `completed` - Завершена
- `cancelled` - Отменена

## Разработка

### Backend разработка

```bash
# Перейти в директорию backend
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn app.main:app --reload
```

### Frontend разработка

```bash
# Перейти в директорию frontend
cd frontend

# Установить зависимости
npm install

# Запустить dev сервер
npm run dev

# Собрать для продакшена
npm run build
npm start
```

## Админ панель

Админ панель находится в разработке. Планируется использование FastAPI Admin для управления:
- Заявками
- Клиентами
- Статусами доставки
- Ценообразованием

## Будущие улучшения

- [ ] Полноценная админ панель
- [ ] Аутентификация администраторов
- [ ] Email уведомления
- [ ] SMS уведомления
- [ ] Интеграция с CRM
- [ ] Калькулятор стоимости
- [ ] Отслеживание грузов
- [ ] Личный кабинет клиента
- [ ] Мультиязычность
- [ ] Новые маршруты (Китай, Европа)

## Production Deploy

Для развертывания в продакшене:

1. Измените переменные окружения в `.env`
2. Настройте SSL сертификаты
3. Используйте Nginx для reverse proxy
4. Настройте резервное копирование БД
5. Настройте мониторинг и логирование

## Лицензия

Proprietary - Все права защищены

## Контакты

Email: info@cargo-express.com
Телефон: +7 (999) 123-45-67
