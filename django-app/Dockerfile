FROM python:3.14-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for database
RUN mkdir -p /data

# Set environment variable for database path
ENV DATABASE_PATH=/data/db.sqlite3

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose application port
EXPOSE 8000

# Declare volume for database persistence
VOLUME ["/data"]

# Run migrations and start gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 2 issuetracker.wsgi:application"]
