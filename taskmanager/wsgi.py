"""
taskmanager/wsgi.py

WSGI (Web Server Gateway Interface) entry point.
This file is used when deploying to a production web server.
For local development we just use: python manage.py runserver
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
application = get_wsgi_application()

