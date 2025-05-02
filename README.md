# Zinochka

![Zinochka - Project Mascot](zinochka.png)

A personal AI-enabled assistant that integrates with Plaud note pin using Zapier.

## Description

Zinochka listens for webhook calls from Zapier with transcripts from Plaud notes, detects activation phrases, extracts tasks using OpenAI agents, and creates them in TickTick using MCP.

## Setup with Docker

1. Set your OpenAI API key in the .env file:
```bash
cp .env.example .env
# Edit .env file with your API key
```

2. Start the application using Docker Compose:
```bash
./start.sh
```

## Manual Setup

1. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Start RabbitMQ:
```bash
# Using Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

4. Run the Celery worker:
```bash
celery -A zinochka.services.celery_app worker --loglevel=info
```

5. Run the server:
```bash
uvicorn zinochka.api.main:app --reload
```

## Architecture

- FastAPI webhook endpoint receiving data from Zapier
- RabbitMQ + Celery for asynchronous task processing
- Activation phrase detection ("зиночка" or "zinochka") 
- Task extraction using OpenAI agents
- TickTick integration via MCP with stdio transport
- Orchestration agent to coordinate task extraction and TickTick integration

## API Endpoints

- `GET /`: Health check endpoint
- `POST /webhook`: Webhook endpoint for receiving transcripts