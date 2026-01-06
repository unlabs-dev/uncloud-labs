# Django Issue Tracker - Tutorial Specification

## Overview

A minimal issue tracker web application designed to demonstrate Django fundamentals in the Uncloud deployment tutorial.

## Goals

- **Demonstrate realistic CRUD operations** with migrations and static assets
- **Keep the codebase small** and tutorial-friendly (~400-500 lines total including templates)
- **Avoid complexity**: No authentication, permissions, or complex workflows
- **Docker-ready**: Runnable with SQLite in a single container, ideal for Uncloud deployment
- **Modern UI**: Simple but visually appealing interface with colors and proper styling
- **Latest Django LTS**: Use Django 5.2 LTS (latest long-term support version)

## Data Models

### Issue Model

Main application model for tracking issues.

**Fields:**

- `title`: `CharField(max_length=200)`
- `description`: `TextField(blank=True)`
- `status`: `CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')`
  - Choices: `OPEN`, `IN_PROGRESS`, `DONE`
- `priority`: `IntegerField(choices=PRIORITY_CHOICES, default=2)`
  - Choices: `1` (Low), `2` (Medium), `3` (High)
- `created_at`: `DateTimeField(auto_now_add=True)`
- `updated_at`: `DateTimeField(auto_now=True)`

**Methods:**

- `__str__()`: Returns the title

### Comment Model

Demonstrates related models and provides a second migration example.

**Fields:**

- `issue`: `ForeignKey(Issue, related_name='comments', on_delete=CASCADE)`
- `author_name`: `CharField(max_length=80)`
- `text`: `TextField()`
- `created_at`: `DateTimeField(auto_now_add=True)`

**Methods:**

- `__str__()`: Returns truncated text with author name

**Note**: Keep comments simple - no edit/delete functionality needed.

### Migration Strategy

1. **Initial migration**: Create Issue model
2. **Second migration**: Add Comment model to demonstrate schema evolution and relationships

## Features & Views

Six simple endpoints to demonstrate full CRUD operations.

### 1. Issue List (Home)

- **URL**: `/`
- **View name**: `issue_list`
- **Method**: GET
- **Features**:
  - Display table of all issues (title, status, priority, created_at)
  - Filter by status via query parameter: `/?status=OPEN`
  - Link to create new issue
  - Links to each issue detail page
- **Template**: `issue_list.html`

### 2. Issue Detail

- **URL**: `/issues/<int:pk>/`
- **View name**: `issue_detail`
- **Method**: GET
- **Features**:
  - Show full issue details (all fields)
  - Display comments in a list (read-only)
  - "Edit" and "Delete" action buttons
- **Template**: `issue_detail.html`

### 3. Create Issue

- **URL**: `/issues/new/`
- **View name**: `issue_create`
- **Methods**: GET (show form), POST (create issue)
- **Features**:
  - Simple form for title, description, priority
  - Status defaults to `OPEN`
  - Validation with error display
  - Redirect to issue detail on success
- **Template**: `issue_form.html`

### 4. Edit Issue

- **URL**: `/issues/<int:pk>/edit/`
- **View name**: `issue_edit`
- **Methods**: GET (show form), POST (update issue)
- **Features**:
  - Pre-populated form with current values
  - Update title, description, status, priority
  - Validation with error display
  - Redirect to issue detail on success
- **Template**: `issue_form.html` (reuse same template as create)

### 5. Delete Issue (Optional)

- **URL**: `/issues/<int:pk>/delete/`
- **View name**: `issue_delete`
- **Methods**: GET (show confirmation), POST (delete issue)
- **Features**:
  - Confirmation page before deletion
  - CSRF protection
  - Redirect to issue list after deletion
- **Template**: `issue_confirm_delete.html`
- **Note**: Can be omitted if keeping CRUD minimal (CRU only)

### 6. Add Comment

- **URL**: `/issues/<int:pk>/comments/add/`
- **View name**: `comment_add`
- **Method**: POST only
- **Features**:
  - Simple form with author_name and text fields
  - CSRF protection
  - Redirect back to issue detail after adding
  - Display form inline on issue detail page
- **Template**: Inline form in `issue_detail.html`

## Implementation Details

### Views

- **Use function-based views (FBVs)** for simplicity and readability
- Use `render()`, `redirect()`, and `get_object_or_404()` shortcuts
- Handle GET and POST in the same view where appropriate

### Forms

Use Django ModelForms for simplicity (easier for beginners):

```python
from django import forms
from .models import Issue, Comment

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
```

**Why ModelForms?**

- Less code to write and maintain
- Automatic validation based on model fields
- Easier to understand for Django beginners
- Standard Django pattern

### Admin Interface

Register models in `admin.py` to provide a full-featured admin interface:

```python
from django.contrib import admin
from .models import Issue, Comment

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['issue', 'author_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author_name', 'text']
```

**Why include admin?**

- Demonstrates Django's built-in admin (a key feature)
- Provides easy data management during development
- Zero extra code in views or templates

## Templates & Static Files

### Template Structure

**`base.html`**

- Page skeleton with `<header>`, `<main>`, `<footer>`
- Includes app title/logo
- Links to CSS: `{% static 'tracker/style.css' %}`
- Defines `{% block content %}` and `{% block title %}`

**`issue_list.html`**

- Extends `base.html`
- Table with issues (responsive design)
- Filter links for each status
- "Create New Issue" button

**`issue_detail.html`**

- Extends `base.html`
- Card layout showing all issue fields
- Status and priority badges (colored appropriately)
- "Edit" and "Delete" action buttons at the top
- Comments section showing all comments for this issue
- Inline form to add a new comment (uses CommentForm)

**`issue_form.html`**

- Extends `base.html`
- Form with proper CSRF token
- Field errors display
- Used for both create and edit (check if issue exists to determine mode)
- Submit button text: "Create Issue" or "Update Issue"
- Cancel button back to detail (edit) or list (create)

**`issue_confirm_delete.html`** (optional)

- Extends `base.html`
- Shows issue details to confirm deletion
- Confirmation form with CSRF token
- "Delete" and "Cancel" buttons

### Static Files

**`tracker/static/tracker/style.css`**

- Modern, visually appealing CSS with:
  - CSS variables for a cohesive color palette (primary, secondary, accent colors)
  - Clean typography with good readability
  - Card-based design with subtle shadows
  - Responsive table design with hover effects
  - Colorful status badges:
    - OPEN: Blue (#3b82f6)
    - IN_PROGRESS: Orange (#f97316)
    - DONE: Green (#22c55e)
  - Priority badges:
    - Low: Gray (#6b7280)
    - Medium: Yellow (#eab308)
    - High: Red (#ef4444)
  - Form styling with proper spacing, focus states, and button animations
  - Mobile-friendly responsive layout with breakpoints
  - Smooth transitions and hover effects
  - Header with gradient or accent color

**Design Inspiration:**

- Clean, minimal aesthetic (think Tailwind-style utility)
- Generous whitespace
- Rounded corners on cards and buttons
- Subtle box shadows for depth
- Color scheme: Use a pleasant palette (e.g., blue primary, warm accents)

## URL Configuration

### App URLs (`tracker/urls.py`)

```python
urlpatterns = [
    path('', views.issue_list, name='issue_list'),
    path('issues/new/', views.issue_create, name='issue_create'),
    path('issues/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issues/<int:pk>/edit/', views.issue_edit, name='issue_edit'),
    path('issues/<int:pk>/delete/', views.issue_delete, name='issue_delete'),  # optional
    path('issues/<int:pk>/comments/add/', views.comment_add, name='comment_add'),
]
```

### Project URLs

- Include tracker URLs at root: `path('', include('tracker.urls'))`
- Include admin: `path('admin/', admin.site.urls)`
- Keep URL structure flat and simple

## Django Settings

### Django Version

- **Django 5.2 LTS** - Latest long-term support release
- Ensures stability and extended support period

### Static Files

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Database

- **SQLite** (`db.sqlite3`) - Simple, file-based database
- No external database server needed
- Perfect for containerized single-instance deployment
- **Data persistence**: Database will be stored in a Docker volume on the remote host
- Database location in container: `/data/db.sqlite3`
- Configure Django `DATABASES` setting to use `/data/db.sqlite3`

### Security & Configuration

- Set `SECRET_KEY` from environment variable (provide a default for development)
- Set `ALLOWED_HOSTS = ['*']` for simplicity (acceptable for tutorial)
- Set `DEBUG = True` for development (better error messages for learning)

### Other Settings

- Configure `DATABASES` to use `/data/db.sqlite3` as the database path
- Keep `INSTALLED_APPS`, `MIDDLEWARE` minimal
- Include only essential Django apps

## Docker Configuration

### Dockerfile

Create a production-ready Dockerfile that:

1. **Base image**: Use Python 3.11 or 3.12 slim image
2. **Working directory**: Set to `/app`
3. **Dependencies**:
   - Copy `requirements.txt` and install packages
   - No need for multi-stage build (keep it simple)
4. **Application code**: Copy all Django project files
5. **Static files**: Run `python manage.py collectstatic --noinput`
6. **Database setup**: Run `python manage.py migrate` as part of startup
7. **Expose port**: Port 8000
8. **Entry point**: Use gunicorn to serve the application
   - Example: `gunicorn --bind 0.0.0.0:8000 project_name.wsgi:application`

### Sample Dockerfile Structure

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create data directory for database
RUN mkdir -p /data

# Expose application port
EXPOSE 8000

# Declare volume for database persistence
VOLUME ["/data"]

# Run migrations and start gunicorn
# Note: Replace 'issuetracker' with your actual project name
CMD python manage.py migrate && \
    gunicorn --bind 0.0.0.0:8000 --workers 2 issuetracker.wsgi:application
```

**Project Structure Note:**

- The project (containing `settings.py` and `wsgi.py`) should be named clearly (e.g., `issuetracker`)
- The app (containing `models.py` and `views.py`) could be named `tracker` or `issues`
- Update the gunicorn command with your actual project name

### requirements.txt

```
Django==5.2.*
gunicorn>=22.0.0
```

### .dockerignore

Include a `.dockerignore` file to exclude unnecessary files:

```
*.pyc
__pycache__/
db.sqlite3
*.sqlite3
.git/
.env
venv/
*.md
```

### Volume Configuration

When deploying the container:

- Mount a Docker volume to `/data` to persist the SQLite database
- The database file (`db.sqlite3`) will be created at `/data/db.sqlite3` on first run
- Application code stays in `/app`, data in `/data` (separate concerns)
- Data persists across container restarts and redeployments
- Example run command: `docker run -v app_data:/data -p 8000:8000 image_name`

## Testing Strategy (Optional)

If including tests for completeness:

- Test Issue model creation and `__str__` method
- Test issue list view returns 200
- Test issue creation via POST
- Test status filtering
- Keep tests minimal (~50-100 lines)

## Success Criteria

The application should:

1. ✅ Run with `python manage.py runserver` locally
2. ✅ Display all CRUD operations working
3. ✅ Show visually appealing, well-styled pages with modern CSS
4. ✅ Build successfully with `docker build`
5. ✅ Run in Docker container with `docker run -p 8000:8000`
6. ✅ Deploy to Uncloud without any configuration changes
7. ✅ Demonstrate migrations working inside the container
8. ✅ Static files served correctly via `collectstatic`
9. ✅ Use Django 5.2 LTS with proper version pinning
10. ✅ SQLite database persists in a Docker volume on the remote host
11. ✅ Data survives container restarts and redeployments

## Out of Scope

To keep the tutorial focused, explicitly exclude:

- ❌ User authentication/registration
- ❌ Authorization/permissions
- ❌ REST API endpoints
- ❌ JavaScript frameworks (React, Vue, etc.)
- ❌ Complex workflows or state machines
- ❌ File uploads
- ❌ Email notifications
- ❌ Celery or background tasks
- ❌ External databases (PostgreSQL, MySQL, etc.) - SQLite only
- ❌ Environment-specific configurations (dev vs prod modes)
- ❌ Comprehensive test suite (basic tests OK)
- ❌ Docker Compose or multi-container setups
