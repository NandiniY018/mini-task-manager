"""
tasks/models.py

This file defines our database table using Python classes.
Each class = one database table.
Each attribute = one column in that table.

Django automatically translates these classes into SQL CREATE TABLE statements.
"""

from django.db import models


class Task(models.Model):
    """
    Represents a single task in the task manager.

    Table name in SQLite: tasks_task
    (Django automatically names it: appname_modelname)
    """

    # --- Priority choices ---
    # Using a tuple of (stored_value, display_label)
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    # --- Status choices ---
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Done', 'Done'),
    ]

    # CharField stores short text; max_length enforces the 100-char rule
    title = models.CharField(max_length=100)

    # TextField stores long text; blank=True makes it optional in Django forms
    # null=True means the database column can be NULL (empty)
    description = models.TextField(blank=True, null=True)

    # Stores one of: 'Low', 'Medium', 'High'
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium',
    )

    # Stores one of: 'Pending', 'Done'; default is 'Pending' as required
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending',
    )

    # DateField stores a date (YYYY-MM-DD), no time component
    due_date = models.DateField()

    # auto_now_add=True means Django sets this automatically when
    # the task is first created. We never set it manually.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Default ordering: newest tasks first
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation shown in Django Admin and shell.
        Returns something like: "Fix login bug (High) - Pending"
        """
        return f"{self.title} ({self.priority}) - {self.status}"

