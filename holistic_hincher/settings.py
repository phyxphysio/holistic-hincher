"""
Django settings for holistic_hincher project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# Environment variables here
DOMAIN = os.getenv('DOMAIN')
DJANGO_ADMIN_USERNAME = os.getenv('DJANGO_ADMIN_USERNAME')
DJANGO_ADMIN_PASSWORD = os.getenv('DJANGO_ADMIN_PASSWORD')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_RECIPIENT = [os.getenv('EMAIL_RECIPIENT'), os.getenv('EMAIL_RECIPIENT_2')]
EMAIL_RECIPIENT = [os.getenv('EMAIL_RECIPIENT'), os.getenv('EMAIL_RECIPIENT_2')]

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEVELOPMENT') in ('True',)

DB_BACKEND = os.getenv('DB_BACKEND')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER','')
DB_PASSWORD = os.getenv('DB_PASSWORD','')
DB_HOST = os.getenv('DB_HOST','')
DB_PORTS = os.getenv('DB_PORTS','')



HOST_IP = os.getenv('HOST_IP')
ALLOWED_HOSTS = ['172.26.21.143', HOST_IP, 'container-service-1.n0von6o0mdks0.ap-southeast-2.cs.amazonlightsail.com', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = [DOMAIN]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "free_pages",
    "ckeditor",
    "ckeditor_uploader",
    "autoslug",
    "mathfilters",
    "django.contrib.sitemaps"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "holistic_hincher.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "holistic_hincher.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": DB_BACKEND,
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORTS": DB_PORTS
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Australia/ACT"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "free_pages/static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = BASE_DIR / "uploads"
MEDIA_URL = "/uploads/"

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": 800,
    },
}

EMAIL_USE_TLS = True

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "/member-resources/"

AUTH_USER_MODEL = "free_pages.CustomUser"  # new
