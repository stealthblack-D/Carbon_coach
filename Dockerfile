# Dockerfile for DevFest 2026 Carbon Coach
# Optimized for Google Cloud Run deployment

FROM python:3.11-slim as base

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specification
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application codebase
COPY . .

# Create non-root user for security best practices
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose standard Cloud Run port
EXPOSE 8080

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run FastAPI server with Uvicorn
CMD ["uvicorn", "carbon_coach.server:app", "--host", "0.0.0.0", "--port", "8080"]
