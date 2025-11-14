FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
# Works with dockerContext: . (root) - copies from backend/requirements.txt
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from backend directory
# Works with dockerContext: . (root) - copies from backend/
COPY backend/ .

# Copy mock_data directory from project root for data initialization
# Works with dockerContext: . (root) - copies from mock_data/
COPY mock_data/ /app/mock_data/

# Expose port
EXPOSE 8000

# Default command (overridden by docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
