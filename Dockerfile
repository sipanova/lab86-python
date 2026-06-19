FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gfortran \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Install Python dependencies first for better layer caching
RUN echo "Installing Python dependencies..."
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Fix ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

CMD ["python", "main.py"]