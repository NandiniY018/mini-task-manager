"""
taskmanager/urls.py

This is the main URL router for the entire Django project.
Every incoming request URL is matched here and sent to the right view.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Django Admin panel: http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),

    # Include all URLs defined in the tasks app
    # e.g. /api/tasks/ -> tasks/urls.py
    path('api/', include('tasks.urls')),

    # Serve the frontend homepage at: http://127.0.0.1:8000/
    # TemplateView looks for index.html in the templates/ folder
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

