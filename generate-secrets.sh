#!/bin/bash

# Скрипт для генерации всех паролей для GitHub Secrets

echo "🔐 Генерация паролей для GitHub Secrets..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📋 Скопируйте эти значения в GitHub Secrets:"
echo ""

echo "SECRET_KEY:"
openssl rand -hex 32
echo ""

echo "POSTGRES_PASSWORD:"
openssl rand -base64 24
echo ""

echo "ADMIN_PASSWORD:"
echo "придумайте сами (например: Admin123!Secure)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Скопируйте значения выше и добавьте в:"
echo "   https://github.com/AmRaul/cargo/settings/secrets/actions"
echo ""
echo "📝 Также добавьте:"
echo "   SERVER_HOST = 5.35.80.213"
echo "   SERVER_USER = root"
echo "   SSH_PRIVATE_KEY = (из команды: cat ~/.ssh/github_cargo)"
echo ""
