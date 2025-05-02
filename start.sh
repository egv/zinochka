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

# Start the services with Docker Compose
docker compose up --build