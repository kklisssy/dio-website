import os
from contextlib import suppress

from .base import *

DEBUG = True
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-development-key",
)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "diowebsite_db"),
        "USER": os.environ.get("POSTGRES_USER", "diowebsite"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "diowebsite12345"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "localhost")
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://localhost:8200")

with suppress(ImportError):
    from .local import *
