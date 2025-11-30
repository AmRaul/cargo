@echo off
echo 🚀 Запуск Cargo Express...
echo.

REM Проверка Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не установлен. Установите Docker Desktop.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose не установлен.
    pause
    exit /b 1
)

echo ✅ Docker найден
echo.

REM Создание .env если не существует
if not exist backend\.env (
    echo 📝 Создание backend\.env из .env.example...
    copy .env.example backend\.env
)

echo 🔨 Сборка и запуск контейнеров...
docker-compose up --build -d

echo.
echo ✅ Все готово!
echo.
echo 📍 Сервисы доступны по адресам:
echo    Frontend:  http://localhost:3000
echo    Backend:   http://localhost:8000
echo    API Docs:  http://localhost:8000/docs
echo.
echo 📊 Просмотр логов: docker-compose logs -f
echo ⏹️  Остановка:     docker-compose down
echo.
pause
