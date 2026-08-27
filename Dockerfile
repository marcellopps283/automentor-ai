# Production Dockerfile for AutoMentor AI on Google Cloud Run
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt pyproject.toml README.md ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copy application code
COPY automentor/ ./automentor/

# Expose Cloud Run port
EXPOSE 8080

# Run FastAPI server
CMD uvicorn automentor.api.server:app --host 0.0.0.0 --port ${PORT}
