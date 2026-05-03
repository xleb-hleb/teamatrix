import os

from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "teamatrix"),
        "USER": os.environ.get("POSTGRES_USER", "teamatrix"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "12345678K"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
