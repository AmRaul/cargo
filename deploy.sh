#!/bin/bash

set -e

echo "🚀 Starting deployment..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo "Please create .env file from .env.production.example"
    exit 1
fi

# Load environment variables
source .env

# Check if ports 80 and 443 are available
echo -e "${YELLOW}🔍 Checking ports availability...${NC}"
if lsof -Pi :80 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Port 80 is already in use${NC}"
    echo "Checking what's using it:"
    lsof -Pi :80 -sTCP:LISTEN || docker ps --filter "publish=80"

    # Try to stop existing nginx container
    if docker ps -q -f name=nginx >/dev/null 2>&1; then
        echo -e "${YELLOW}🛑 Stopping existing nginx container...${NC}"
        docker stop nginx 2>/dev/null || true
        docker rm nginx 2>/dev/null || true
    fi
fi

echo -e "${YELLOW}📥 Pulling latest changes...${NC}"
git pull origin main 2>/dev/null || echo "Skipping git pull (running from GitHub Actions)"

echo -e "${YELLOW}🛑 Stopping existing cargo containers...${NC}"
docker-compose -f docker-compose.prod.yml down

# Force stop any containers using ports 80/443
echo -e "${YELLOW}🧹 Cleaning up port conflicts...${NC}"
for port in 80 443; do
    container_id=$(docker ps -q --filter "publish=$port" 2>/dev/null)
    if [ ! -z "$container_id" ]; then
        echo -e "${YELLOW}⚠️  Stopping container using port $port: $container_id${NC}"
        docker stop $container_id 2>/dev/null || true
    fi
done

echo -e "${YELLOW}🗑️  Cleaning up old images...${NC}"
docker system prune -f

echo -e "${YELLOW}🔨 Building containers...${NC}"
docker-compose -f docker-compose.prod.yml build

echo -e "${YELLOW}🚀 Starting containers...${NC}"
docker-compose -f docker-compose.prod.yml up -d

echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 10

# Check if containers are running
if [ "$(docker ps -q -f name=cargo_backend_prod)" ]; then
    echo -e "${GREEN}✅ Backend is running${NC}"
else
    echo -e "${RED}❌ Backend failed to start${NC}"
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
fi

if [ "$(docker ps -q -f name=cargo_frontend_prod)" ]; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
else
    echo -e "${RED}❌ Frontend failed to start${NC}"
    docker-compose -f docker-compose.prod.yml logs frontend
    exit 1
fi

# Check nginx only if it's defined in docker-compose
if docker-compose -f docker-compose.prod.yml config --services | grep -q "^nginx$"; then
    if [ "$(docker ps -q -f name=cargo_nginx)" ]; then
        echo -e "${GREEN}✅ Nginx is running${NC}"
    else
        echo -e "${RED}❌ Nginx failed to start${NC}"
        docker-compose -f docker-compose.prod.yml logs nginx
        exit 1
    fi
else
    echo -e "${YELLOW}ℹ️  Nginx not included (using external nginx)${NC}"
fi

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Site is available at: https://hub-cargo.ru${NC}"

# Show running containers
echo -e "\n${YELLOW}📊 Running containers:${NC}"
docker-compose -f docker-compose.prod.yml ps
