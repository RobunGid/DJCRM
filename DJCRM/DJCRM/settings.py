from pathlib import Path
from dotenv import dotenv_values

ENV_VALUES = dotenv_values("../.env")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&y_y*orlwsuul-xbr#!0$b^#v$8-!yr4jubm+qr(dlp$!i-c+v'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'users',
    'dashboard',
    'leads',
    'clients',
    'teams',
    'products',
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "unfold.contrib.location_field",  # optional, if django-location-field package is used
    "unfold.contrib.constance",  # optional, if django-constance package is used
    'django.contrib.admin',
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

ROOT_URLCONF = 'DJCRM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'teams.context_processors.team'
            ],
        },
    },
]

WSGI_APPLICATION = 'DJCRM.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
	BASE_DIR / 'static',
]

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "users:login"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST_PASSWORD = ENV_VALUES["EMAIL_HOST_PASSWORD"]
EMAIL_HOST = ENV_VALUES["EMAIL_HOST"]
EMAIL_PORT = ENV_VALUES["EMAIL_PORT"]
EMAIL_HOST_USER = ENV_VALUES["EMAIL_HOST_USER"]
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER