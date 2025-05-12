# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY dependencies.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r dependencies.txt

# Copy project files, excluding the SQLite database
COPY . .
RUN rm -f /app/instance/diary.db

# Create a non-root user to run the app
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Create volume for SQLite database (if using SQLite)
VOLUME ["/app/instance"]

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "main:app"]