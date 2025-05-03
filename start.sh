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

# Load variables from .env file
if [ -f .env ]; then
    # Extract EMAIL and WEBHOOK_DOMAIN from .env file
    EMAIL=$(grep -o '^EMAIL=.*' .env | cut -d= -f2)
    WEBHOOK_DOMAIN=$(grep -o '^WEBHOOK_DOMAIN=.*' .env | cut -d= -f2)
    
    # Update Traefik configuration if variables are found
    if [ -n "$EMAIL" ] && [ -n "$WEBHOOK_DOMAIN" ]; then
        sed -i.bak "s/your-email@example.com/$EMAIL/g" traefik/config/traefik.yml
        sed -i.bak "s/webhook.yourdomain.com/$WEBHOOK_DOMAIN/g" docker-compose.yml
        echo "Using configuration from .env file: domain=$WEBHOOK_DOMAIN, email=$EMAIL"
    else
        echo "Warning: EMAIL or WEBHOOK_DOMAIN not found in .env file"
    fi
fi

# Create necessary directories for Traefik
mkdir -p traefik/config/dynamic_conf

# Clean previous certificate data if requested
if [ "$1" = "--reset-certs" ]; then
    echo "Removing previous Traefik certificates..."
    docker volume rm zinochka_traefik-certificates || true
fi

# Start the services with Docker Compose
docker compose up --build