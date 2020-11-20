"""
This contains the settings for this project, it is supposed to be kept in
jiezi_secret and never committed to public git
"""

import os
from jiezi_secret import secret # this is jiezi secret file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.SECRET_KEY

try:
    DEBUG = secret.DEBUG # this is set to true on production server
except AttributeError:
    DEBUG = True
SESSION_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG

if not DEBUG:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration

        sentry_sdk.init(
            dsn="https://8f1f521c155c42b5be26ae38e24f330a@o479182.ingest.sentry.io/5523357",
            integrations=[DjangoIntegration()],
            traces_sample_rate=1.0,

            # If you wish to associate users to errors (assuming you are using
            # django.contrib.auth) you may enable sending PII data.
            send_default_pii=True
        )
    except ModuleNotFoundError:
        pass

try:
    ALLOWED_HOSTS = secret.ALLOWED_HOSTS
except AttributeError:
    ALLOWED_HOSTS = ['127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'rest_framework',
    'django_fsm',
    'django_bootstrap_breadcrumbs',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # celery apps
    'celery',
    'celery_progress',

    # custom apps
    'accounts',
    'learning',
    'content',
    'classroom',
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

ROOT_URLCONF = 'jiezi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        'libraries': {
                'my_tags': 'jiezi.template_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'jiezi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    # this is the database for server, and connection is only allowed within
    # internal network, set up your own database and change jiezi_secret setting
    # accordingly
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'jiezi',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
try:
    DATABASES.update(secret.DATABASES)
except AttributeError:
    pass

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')


LOGIN_REDIRECT_URL='/'
AUTH_USER_MODEL='accounts.User'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CSRF_USE_SESSIONS = True
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Celery Settings
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_METADATA_CLASS': 'jiezi.rest.metadata.CustomActionsMetadata',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'jiezi.rest.renderers.CustomActionsBrowsableAPIRenderer',
    ],
}

ADMINS = [('chenyx', 'chenyx@solvedchinese.org')]
MANAGERS = [('chenyx', 'chenyx@solvedchinese.org')]

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
try:
    EMAIL_HOST = secret.EMAIL_HOST
    EMAIL_PORT = secret.EMAIL_PORT
    EMAIL_HOST_USER = secret.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD
except AttributeError:
    pass
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = '解字 Solved Chinese<noreply@solvedchinese.org>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

""" Here begins jiezi custom settings """
# put the secert key in this path
DATAFILE_SERVICE_ACCOUNT_FILE_PATH = os.path.join(BASE_DIR,
    'jiezi_secret/datafile_service_account.json')
