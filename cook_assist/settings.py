import os
from pathlib import Path


# ====================================================================
# 🔄 LOCAL DEV MODE - SWITCH 1: UNCOMMENT THIS BLOCK FOR LOCAL RUNNING
# ====================================================================
IS_LOCAL_DEV = True
if 'IS_LOCAL_DEV' in locals() and IS_LOCAL_DEV:
    # 1. Set DEBUG to True for detailed errors and static file handling
    DEBUG = True
    # 2. Allow local hosts
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    # 3. Allow local origin for CSRF checks
    CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']
# ====================================================================


# ====================================================================
# ⚠️ RENDER PROD MODE - CSRF_TRUSTED_ORIGINS: COMMENT OUT for local
# ====================================================================
# CSRF_TRUSTED_ORIGINS = [
#     'https://cooking-assistant-h2w8.onrender.com',
# ]

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-insecure-key')

# ====================================================================
# ⚠️ RENDER PROD MODE - DEBUG: COMMENT OUT for local
# ====================================================================
# DEBUG = False

# ====================================================================
# ⚠️ RENDER PROD MODE - ALLOWED_HOSTS: COMMENT OUT for local
# ====================================================================
# ALLOWED_HOSTS = ['cooking-assistant-h2w8.onrender.com']


RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

# if RENDER_EXTERNAL_HOSTNAME:
#     ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
#     ALLOWED_HOSTS.append('.onrender.com')


INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'recipes',
    'feedback',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cook_assist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cook_assist.wsgi.application'


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

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'