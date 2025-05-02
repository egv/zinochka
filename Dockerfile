FROM python:3.11-slim

WORKDIR /app

# Install UV for Python package management
RUN pip install uv

# Install application requirements
COPY pyproject.toml .
COPY README.md .

# Create a virtual environment and install dependencies
RUN uv pip install -e .

# Copy the application code
COPY zinochka ./zinochka
COPY tests ./tests

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run when the container starts
CMD ["uvicorn", "zinochka.api.main:app", "--host", "0.0.0.0", "--port", "8000"]