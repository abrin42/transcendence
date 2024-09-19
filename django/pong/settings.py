"""
Django settings for pong project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os, json, datetime
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {setting} environment variable.")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']


# CSRF settings
CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pyotp',
    'friend',
    'player',
    'game',

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

ROOT_URLCONF = 'pong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'pong.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': "django",

        'USER': "django",

        'PASSWORD': "django",

        'HOST': "postgresql",

        'PORT': "5432",

    }

}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'player.Player'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

#Custom user model
LOGIN_URL = "player/login/"

# 42 API
FT42_CLIENT_ID = get_secret('FT42_client_id')
FT42_CLIENT_SECRET = get_secret('FT42_client_secret')
FT42_REDIRECT_URI = get_secret('FT42_redirect_uri')
FT42_OAUTH_URL = get_secret('FT42_0auth_url')

# Vonage API
VONAGE_API_KEY = get_secret('vonage_api_key')
VONAGE_SECRET_KEY = get_secret('vonage_secret_key')

# SMTP Server Configuration
SMTP_SERVER = get_secret('smtp_server')
SMTP_PORT = get_secret('smtp_port')
SMTP_USERNAME = get_secret('smtp_username')
SMTP_PASSWORD = get_secret('smtp_password')

# JWT
JWT_SECRET_KEY = get_secret('jwt_secret_key')
JWT_ALGORITHM = get_secret('jwt_algo')
JWT_EXP_DELTA_SECONDS = get_secret('jwt_exp')
