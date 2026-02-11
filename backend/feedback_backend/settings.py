"""Django settings for feedback_backend project (minimal for API).

This file intentionally keeps settings minimal to make it easy to run locally.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'replace-me-in-prod'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'feedback_backend.urls'

TEMPLATES = []

WSGI_APPLICATION = 'feedback_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# Allow CORS from the React dev server during development
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

# Alternatively allow all origins in DEBUG mode
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
