"""
tasks/admin.py

Registers our Task model with Django's built-in Admin panel.
After this, you can manage tasks at: http://127.0.0.1:8000/admin/
"""

from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Customises how Tasks appear in the Django Admin interface.
    """
    # Columns shown in the task list view
    list_display = ('title', 'priority', 'status', 'due_date', 'created_at')

    # Sidebar filters on the right side of the admin list
    list_filter = ('status', 'priority')

    # Enable search by title or description
    search_fields = ('title', 'description')

    # Default sort order in admin
    ordering = ('-created_at',)

