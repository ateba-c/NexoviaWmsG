from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


def env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


SECRET_KEY = env("DJANGO_SECRET_KEY", "unsafe-dev-secret")
DEBUG = env("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [host.strip() for host in env("DJANGO_ALLOWED_HOSTS", "localhost").split(",")]

SHARED_APPS = [
    "django_tenants",
    "apps.tenants",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "django_filters",
    "channels",
]

TENANT_APPS = [
    "apps.accounts",
    "apps.warehouse",
    "apps.items",
    "apps.inventory",
    "apps.inbound",
    "apps.outbound",
    "apps.shipping",
    "apps.returns",
    "apps.counting",
    "apps.lpn",
    "apps.labels",
    "apps.integrations",
    "apps.analytics",
    "apps.ai",
    "apps.notifications",
    "apps.audit",
]

INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_tenants.middleware.main.TenantMainMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.audit.middleware.AuditMiddleware",
]

ROOT_URLCONF = "config.urls"
PUBLIC_SCHEMA_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": env("POSTGRES_DB", "nexoflow"),
        "USER": env("POSTGRES_USER", "nexoflow"),
        "PASSWORD": env("POSTGRES_PASSWORD", "dev_password"),
        "HOST": env("POSTGRES_HOST", "localhost"),
        "PORT": env("POSTGRES_PORT", "5432"),
    }
}

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)
TENANT_MODEL = "tenants.Tenant"
TENANT_DOMAIN_MODEL = "tenants.Domain"
AUTH_USER_MODEL = "accounts.User"

LANGUAGE_CODE = "en-ca"
LANGUAGES = [
    ("en-ca", "English (Canada)"),
    ("fr-ca", "French (Canada)"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "America/Toronto"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(env("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", "30"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(env("JWT_REFRESH_TOKEN_LIFETIME_DAYS", "1"))),
    "SIGNING_KEY": env("JWT_SIGNING_KEY", SECRET_KEY),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "NexoFlow WMS API",
    "DESCRIPTION": "Warehouse Management System API",
    "VERSION": "1.0.0",
}

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in env("DJANGO_CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

REDIS_URL = env("REDIS_URL", "redis://localhost:6379/0")
REDIS_CHANNEL_URL = env("REDIS_CHANNEL_URL", "redis://localhost:6379/1")

OPENAI_API_KEY = env("OPENAI_API_KEY", "")
OPENAI_MODEL = env("OPENAI_MODEL", "gpt-5")
OPENAI_SYSTEM_PROMPT = env(
    "OPENAI_SYSTEM_PROMPT",
    (
        "You are the NexoFlow warehouse copilot. Provide concise, actionable guidance for warehouse execution, "
        "inventory control, inbound, outbound, counting, shipping, and tenant-safe operations."
    ),
)

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_ROUTES = {
    "apps.labels.tasks.*": {"queue": "labels"},
    "apps.notifications.tasks.*": {"queue": "high"},
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_CHANNEL_URL]},
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
