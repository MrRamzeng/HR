import os
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(find_dotenv())

SECRET_KEY = get_random_secret_key()

DEBUG = True

ALLOWED_HOSTS = ['mrramzeng.pythonanywhere.com', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'game.apps.GameConfig',
    'main.apps.MainConfig',
    'user.apps.UserConfig',
    'nested_admin',
    'compressor'
]

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HandRead.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'HandRead.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env.get('ENGINE'),
        'NAME': env.get('DB'),
        'PASSWORD': env.get('DB_PASSWORD')
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttribute'
                'SimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLength'
                'Validator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPassword'
                'Validator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPassword'
                'Validator',
    },
]

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = env.get('EMAIL_HOST')

EMAIL_PORT = env.get('EMAIL_PORT')

EMAIL_USE_TLS = env.get('EMAIL_TLS')

EMAIL_HOST_USER = env.get('EMAIL')

EMAIL_HOST_PASSWORD = env.get('PASSWORD')

EMAIL_SERVER = EMAIL_HOST_USER

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_ADMIN = EMAIL_HOST_USER

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = False

STATIC_URL = 'static/'

COMPRESS_ROOT = STATIC_URL

COMPRESS_ENABLED = True

STATICFILES_FINDERS = 'compressor.finders.CompressorFinder',

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
