#!/bin/bash

# Script to initialize SSL certificates for hub-cargo.ru

set -e

DOMAIN="hub-cargo.ru"
EMAIL="your-email@example.com"  # CHANGE THIS!

echo "🔒 Initializing SSL certificates for $DOMAIN..."

# Create temporary nginx config for certificate challenge
cat > nginx/conf.d/cargo-temp.conf << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name hub-cargo.ru www.hub-cargo.ru;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
EOF

# Rename production config temporarily
if [ -f nginx/conf.d/cargo.conf ]; then
    mv nginx/conf.d/cargo.conf nginx/conf.d/cargo.conf.bak
fi

echo "🚀 Starting nginx for certificate challenge..."
docker-compose -f docker-compose.prod.yml up -d nginx

echo "⏳ Waiting for nginx to start..."
sleep 5

echo "📜 Requesting SSL certificate..."
docker-compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

echo "🔄 Restoring production nginx config..."
rm nginx/conf.d/cargo-temp.conf
if [ -f nginx/conf.d/cargo.conf.bak ]; then
    mv nginx/conf.d/cargo.conf.bak nginx/conf.d/cargo.conf
fi

echo "♻️  Reloading nginx..."
docker-compose -f docker-compose.prod.yml restart nginx

echo "✅ SSL certificates initialized successfully!"
echo "🔒 Certificates location: ./certbot/conf/live/$DOMAIN/"
