"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import sys
from pathlib import Path

import environ
from loguru import logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
root = environ.Path(__file__) - 3  # get root of the project

env = environ.Env()
env.read_env(BASE_DIR.joinpath(".env"))  # reading .env file

logger.debug(f"ProcessId {os.getpid()}")
logger.debug(f"RootDir: {root}")
logger.debug(f"BaseDir: {BASE_DIR}")
logger.debug(f"TemplatesDir: {BASE_DIR.joinpath('src/templates')}")

ENV = env.str("ENV", default="local")
logger.debug(f"ENV: {ENV}")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", default="")
logger.debug(f"SECRET_KEY: {SECRET_KEY}")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)
logger.debug(f"DEBUG: {DEBUG}")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
logger.debug(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    ## features
    "corsheaders",
    "django_browser_reload",
    "django_softdelete",
    "taggit",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # "drf_yasg",
    # "rest_framework.authtoken",
    # "dj_rest_auth",
    # "dj_rest_auth.registration",
    ## ui
    "django_bootstrap5",
    "django_bootstrap_icons",
    "crispy_forms",
    "crispy_bootstrap5",
    # 'tailwind',
    # 'theme',
    # "imagekit",
    "phonenumber_field",
    ## apps
    "apps.core",
    "apps.users",
    "apps.auths",
    "apps.data",
    "apps.home",
    "apps.bio",
    "apps.dashboard",
    "apps.dictionary",
    # "apps.quran",
    "apps.todo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # higher stack
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # features
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.joinpath("src/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        "ENGINE": "django.db.backends.mysql",
        "NAME": env.str("MYSQL_DATABASE", default=""),
        "USER": env.str("MYSQL_USER", default=""),
        "PASSWORD": env.str("MYSQL_PASSWORD", default=""),
        "HOST": env.str("MYSQL_HOST", default=""),  # db for docker container name; 127.0.0.1 for terminal
        "PORT": env.str("MYSQL_PORT", default=""),
        "OPTIONS": {"charset": "utf8mb4", "use_unicode": True, "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        "TEST": {
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# for initial keeping static files
STATIC_URL = "src/static/"
# for storing collected static files
STATIC_ROOT = (
    BASE_DIR.joinpath("src/staticfiles") if ENV == "local" else "/home/iamromandev/public_html/web/django/staticfiles"
)
# for collecting images also
STATICFILES_DIRS = [
    BASE_DIR.joinpath("src/static"),
]
MEDIA_URL = "src/media/"
MEDIA_ROOT = (
    BASE_DIR.joinpath("src/mediafiles") if ENV == "local" else "/home/iamromandev/public_html/web/django/mediafiles"
)


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# tailwind
# TAILWIND_APP_NAME = 'theme'
# INTERNAL_IPS = [
#     '127.0.0.1',
# ]
# if not DEBUG:
#     NPM_BIN_PATH = '/home/iamromandev/nodevenv/repositories/web/django/src/theme/static_src/14/bin/npm'

# django bootstrap icons
BS_ICONS_CUSTOM_PATH = "icons"
BS_ICONS_CACHE = os.path.join(STATIC_ROOT, "cache-icons")

# django taggit
TAGGIT_CASE_INSENSITIVE = True

# custom auth user model
AUTH_USER_MODEL = "core.User"

# loguru
logger.remove()

logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{"
    "function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    backtrace=True,
    diagnose=True,
)

# rest framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework.authentication.BasicAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
        # "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    # 'EXCEPTION_HANDLER': 'core.libs.custom_exception_handler',
    "PAGE_SIZE": 10,
}

# authentication
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # "allauth.account.auth_backends.AuthenticationBackend",
]

# dj_rest_auth
# REST_AUTH = {
#    "USE_JWT": True,
#   "JWT_AUTH_COOKIE": "auth-cookie",
#   "JWT_AUTH_REFRESH_COOKIE": "auth-refresh-cookie",
# }

SITE_ID = env.int("SITE_ID", default=1)
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", default=True)

# ui
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# simple_jwt

# dictionary
WORDNIK_API_KEYS = env.list("WORDNIK_API_KEYS", default=[])
logger.debug(f"WORDNIK_API_KEYS: {WORDNIK_API_KEYS}")

TRANSLATION_ENABLED = env.bool("TRANSLATION_ENABLED", default=False)
logger.debug(f"TRANSLATION_ENABLED: {TRANSLATION_ENABLED}")
