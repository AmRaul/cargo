#!/bin/bash

echo "🚀 Запуск Cargo Express..."
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker Desktop."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен."
    exit 1
fi

echo "✅ Docker найден"
echo ""

# Создание .env если не существует
if [ ! -f backend/.env ]; then
    echo "📝 Создание backend/.env из .env.example..."
    cp .env.example backend/.env
fi

echo "🔨 Сборка и запуск контейнеров..."
docker-compose up --build -d

echo ""
echo "✅ Все готово!"
echo ""
echo "📍 Сервисы доступны по адресам:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📊 Просмотр логов: docker-compose logs -f"
echo "⏹️  Остановка:     docker-compose down"
echo ""
