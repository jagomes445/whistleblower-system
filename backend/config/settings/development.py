"""
Development settings for whistleblower project.
"""
from .base import *

DEBUG = True

# Development-specific settings
INSTALLED_APPS += [
    'django_extensions',
]

# Disable password validation in development
AUTH_PASSWORD_VALIDATORS = []

# Email backend for development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
