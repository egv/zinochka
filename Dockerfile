FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install application requirements
COPY pyproject.toml .
COPY README.md .

# Create a virtual environment and install dependencies
RUN uv sync 

# Copy the application code
COPY zinochka ./zinochka
COPY tests ./tests

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run when the container starts
CMD ["uv", "run", "uvicorn", "zinochka.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
