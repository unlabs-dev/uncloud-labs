from django.contrib import admin
from .models import Issue, Comment


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """Admin interface for Issue model."""
    list_display = ['title', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""
    list_display = ['issue', 'author_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author_name', 'text']
