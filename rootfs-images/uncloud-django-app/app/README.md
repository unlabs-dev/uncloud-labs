# Django Issue Tracker

A minimal, modern issue tracking web application built with Django 5.2 LTS.

## Features

- ✅ Full CRUD operations for issues
- ✅ Status tracking (Open, In Progress, Done)
- ✅ Priority levels (Low, Medium, High)
- ✅ Comment system for issues
- ✅ Modern, responsive UI
- ✅ Django admin interface
- ✅ Docker-ready with data persistence

## Quick Start

### Local Development

```bash
# Install dependencies
uv sync

# Run migrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Run server
uv run python manage.py runserver
```

Visit http://localhost:8000/

### Docker Deployment

```bash
# Build image
docker build -t issue-tracker .

# Run with volume persistence
docker run -d -p 8000:8000 -v issue-tracker-data:/data issue-tracker
```

## Tech Stack

- Django 5.2 LTS
- SQLite with Docker volume persistence
- Gunicorn WSGI server
- Python 3.12
- Modern CSS

## Documentation

See `SPEC.md` for complete specification.
