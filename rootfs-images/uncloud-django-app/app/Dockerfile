# Use Python 3.14 as the base image
FROM python:3.14-slim

# Set up the working directory
WORKDIR /app

# Install helper system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Create data directory for database and set ownership
RUN mkdir -p /data && chown appuser:appuser /data

# Set environment variable for database path
ENV DATABASE_PATH=/data/db.sqlite3

# Copy application code
COPY --chown=appuser:appuser . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Declare volume for database persistence
VOLUME ["/data"]

# Run database migrations and start Gunicorn application server
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 2 issuetracker.wsgi:application"]
