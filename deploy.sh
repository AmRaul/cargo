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

echo -e "${YELLOW}📥 Pulling latest changes...${NC}"
git pull origin main

echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
docker-compose -f docker-compose.prod.yml down

echo -e "${YELLOW}🗑️  Cleaning up old images...${NC}"
docker system prune -f

echo -e "${YELLOW}🔨 Building containers...${NC}"
docker-compose -f docker-compose.prod.yml build --no-cache

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

if [ "$(docker ps -q -f name=cargo_nginx)" ]; then
    echo -e "${GREEN}✅ Nginx is running${NC}"
else
    echo -e "${RED}❌ Nginx failed to start${NC}"
    docker-compose -f docker-compose.prod.yml logs nginx
    exit 1
fi

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Site is available at: https://hub-cargo.ru${NC}"

# Show running containers
echo -e "\n${YELLOW}📊 Running containers:${NC}"
docker-compose -f docker-compose.prod.yml ps
