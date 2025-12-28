#!/bin/bash

# Cargo Logistics - Quick Start Script

echo "🚚 Cargo Logistics Accounting System"
echo "===================================="
echo ""

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker and Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and change passwords before deploying to production!"
    echo ""
    read -p "Press Enter to continue with default values, or Ctrl+C to edit .env first..."
fi

echo "📦 Building and starting containers..."
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

echo ""
echo "📊 Creating initial test data..."
docker-compose exec -T backend python create_initial_data.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Available URLs:"
echo "   Admin Panel: http://localhost:8000/admin"
echo "   API Docs:    http://localhost:8000/docs"
echo "   API Root:    http://localhost:8000"
echo ""
echo "🔐 Admin credentials (from .env):"
echo "   Username: admin"
echo "   Password: \$ADMIN_PASSWORD (check your .env file)"
echo ""
echo "⚠️  SECURITY WARNING:"
echo "   - Change ADMIN_PASSWORD in .env for production!"
echo "   - Change SECRET_KEY in .env for production!"
echo "   - Never commit .env file to git!"
echo ""
echo "📋 Useful commands:"
echo "   View logs:        docker-compose logs -f backend"
echo "   Stop services:    docker-compose down"
echo "   Restart:          docker-compose restart"
echo "   Clean DB:         docker-compose down -v"
echo ""
