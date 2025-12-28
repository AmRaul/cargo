#!/bin/bash

set -e  # Exit on error

echo "⏳ Waiting for PostgreSQL to be ready..."
while ! pg_isready -h postgres -U ${POSTGRES_USER:-cargo_user} -d ${POSTGRES_DB:-cargo_db} > /dev/null 2>&1; do
  sleep 1
done
echo "✅ PostgreSQL is ready"

echo "🔄 Running Alembic migrations..."
alembic upgrade head
echo "✅ Migrations applied"

# Optional: Create initial data if needed (uncomment if you want)
# echo "📊 Creating initial data..."
# python create_initial_data.py || echo "⚠️  Initial data already exists or error occurred"

# Check if running in production
if [ "${ENVIRONMENT}" = "production" ]; then
    echo "🚀 Starting FastAPI server (PRODUCTION mode with 4 workers)..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
else
    echo "🛠️  Starting FastAPI server (DEVELOPMENT mode with reload)..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi
