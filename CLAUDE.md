# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Test Commands
- Install dependencies: `uv pip install -e .`
- Run tests: `pytest`
- Run single test: `pytest path/to/test.py::test_function_name -v`
- Lint code: `ruff check .`
- Type check: `mypy .`

## Code Style Guidelines
- Use Python with FastAPI for web server implementation
- Follow TDD: write tests first, then code to make tests pass
- Use Pydantic for data validation and parsing
- Format code with Black and sort imports with isort
- Use type hints everywhere
- Use snake_case for variables and functions, PascalCase for classes
- Error handling: use try/except blocks with specific exceptions
- Document all functions and classes with docstrings
- Package management: Always use `pyproject.toml` instead of `requirements.txt`
- Use `uv` for all Python-related tasks
- Use `gh` tool for all GitHub interactions

## Project-Specific Notes
- Main application processes webhook data from Plaud notes
- Webhook endpoint puts transcript data into Celery task queue
- Task processing pipeline:
  1. Check for activation phrase "зиночка" or "zinochka" in the transcript
  2. If found, process with orchestration agent
  3. Orchestration agent uses task extraction agent to identify tasks
  4. Tasks are created in TickTick using MCP with stdio transport
- Implementation uses agent-to-agent communication via agent.as_tool()
- Tests are mocked to avoid actual API calls to OpenAI
- Docker Compose setup for easy deployment

## Docker Commands
- Start all services: `./start.sh`
- Run tests in Docker: `docker compose run api pytest`
- View logs: `docker compose logs -f`