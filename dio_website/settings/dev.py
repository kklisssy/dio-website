import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

FASTAPI_RAG = os.environ.get("FASTAPI_RAG")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "localhost")
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://localhost:8002")

try:
    from .local import *
except ImportError:
    pass
