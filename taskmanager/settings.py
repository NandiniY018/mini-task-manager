"""
taskmanager/settings.py

Django configuration file.
All project-wide settings live here — database, apps, static files, etc.
"""

import os
from pathlib import Path

# ------------------------------------------------------------
# Base directory – the root of the project (where manage.py is)
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------
# Security
# ------------------------------------------------------------
# SECURITY WARNING: keep the secret key secret in production!
SECRET_KEY = 'django-insecure-florix-task-manager-secret-key-2024-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow requests from localhost only
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# ------------------------------------------------------------
# Application definition
# Django needs to know about all installed apps.
# ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',       # Admin panel at /admin/
    'django.contrib.auth',        # User login/logout system
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Serve CSS/JS files
    'tasks',                      # Our custom app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------
# URL configuration entry point
# ------------------------------------------------------------
ROOT_URLCONF = 'taskmanager.urls'

# ------------------------------------------------------------
# Template settings – tells Django where to find HTML files
# ------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Look for templates in a top-level "templates/" folder
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'taskmanager.wsgi.application'

# ------------------------------------------------------------
# Database – using SQLite (file-based, no server needed)
# ------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # db.sqlite3 file is created in the project root
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------------------------
# Password validation & hashers
# ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

# ------------------------------------------------------------
# Localisation
# ------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True  # Store timestamps in UTC in the database

# ------------------------------------------------------------
# Static files (CSS, JavaScript)
# STATIC_URL is the URL prefix for static files in the browser.
# STATICFILES_DIRS tells Django where to find static files on disk.
# ------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ------------------------------------------------------------
# Default primary key type for models
# ------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

