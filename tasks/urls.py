"""
tasks/urls.py

URL patterns specifically for the tasks app.
These are "mounted" under /api/ in the main taskmanager/urls.py.

So the full URLs become:
  /api/tasks/       → task_list view
  /api/tasks/<id>/  → task_detail view
"""

from django.urls import path
from . import views

urlpatterns = [
    # Matches: /api/tasks/
    path('tasks/', views.task_list, name='task-list'),

    # Matches: /api/tasks/1/  or  /api/tasks/42/  etc.
    # <int:task_id> captures the integer ID from the URL
    # and passes it as the task_id parameter to the view function
    path('tasks/<int:task_id>/', views.task_detail, name='task-detail'),
]

