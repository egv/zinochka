#!/bin/bash

# Ensure .env file exists
if [ ! -f .env ]; then
    echo "No .env file found. Creating from example..."
    cp .env.example .env
    echo "Please edit .env file with your OpenAI API key before continuing."
    exit 1
fi

# Check if .env is different from .env.example
if diff -q .env .env.example > /dev/null; then
    echo "Error: .env file appears to be unchanged from .env.example"
    echo "Please edit .env file with your actual OpenAI API key before continuing."
    exit 1
fi

# Update domain in Traefik configuration
read -p "Enter your domain for the webhook (e.g., webhook.example.com): " WEBHOOK_DOMAIN
read -p "Enter your email for Let's Encrypt notifications: " EMAIL

# Update Traefik configuration
sed -i.bak "s/webhook.yourdomain.com/$WEBHOOK_DOMAIN/g" docker-compose.yml
sed -i.bak "s/your-email@example.com/$EMAIL/g" traefik/config/traefik.yml

echo "Configuration updated for domain: $WEBHOOK_DOMAIN"

# Create necessary directories for Traefik
mkdir -p traefik/config/dynamic_conf

# Start the services with Docker Compose
docker compose up --build