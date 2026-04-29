#!/bin/bash
set -e

DOMAIN="chatbotg9.duckdns.org"
EMAIL="tarikfetahovic1309@gmail.com"
CERTBOT_DIR="./nginx/certbot"

mkdir -p "$CERTBOT_DIR/conf/live/$DOMAIN" "$CERTBOT_DIR/www"

# Download recommended TLS parameters from certbot
if [ ! -e "$CERTBOT_DIR/conf/options-ssl-nginx.conf" ]; then
    echo "Downloading TLS parameters..."
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf \
        > "$CERTBOT_DIR/conf/options-ssl-nginx.conf"
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem \
        > "$CERTBOT_DIR/conf/ssl-dhparams.pem"
fi

# Create a temporary self-signed cert so nginx can start before we have a real cert
echo "Creating temporary self-signed certificate..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml run --rm --entrypoint \
    "openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
     -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
     -out    /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
     -subj   /CN=localhost" \
    certbot

# Start nginx (needs a cert to exist, even a dummy one)
echo "Starting nginx..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --force-recreate -d nginx

# Remove dummy cert and get the real one
echo "Obtaining Let's Encrypt certificate for $DOMAIN..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml run --rm --entrypoint \
    "certbot certonly --webroot -w /var/www/certbot \
     --email $EMAIL -d $DOMAIN \
     --rsa-key-size 4096 \
     --agree-tos \
     --force-renewal" \
    certbot

# Reload nginx to pick up the real cert
echo "Reloading nginx..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec nginx nginx -s reload

echo ""
echo "Done! Certificate obtained for $DOMAIN"
echo "Now start all services with:"
echo "  docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d"
