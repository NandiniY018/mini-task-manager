#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
Run this file to interact with your Django project.
Example: python manage.py runserver
"""
import os
import sys


def main():
    """Run administrative tasks."""
    # Tell Django which settings file to use
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

