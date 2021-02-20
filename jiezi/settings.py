"""
This contains the default settings for this project,
for local / secret settings, please put under jiezi_secret.secret,
which will overwrite this file (see file end)
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# use this function to generate a secret key
# from django.core.management.utils import get_random_secret_key
# and put it under your secret file
SECRET_KEY = 'm$0#1ups4&_x0xti^mjs=2eqgcqex0nlbo01s02zo6b&o68+)2'

DEBUG = True
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False


# by default, we redirect all media to dev, set to None if not needed
MEDIA_REDIRECT = 'https://dev.solvedchinese.org/media/'


ALLOWED_HOSTS = ['127.0.0.1','localhost']


# Application definition
INSTALLED_APPS = [
    'dal', # make sure dal appear before django.contrib.admin
    'dal_select2',
    'dal_queryset_sequence',
    'rest_framework',
    'django_bootstrap_breadcrumbs',
    'logentry_admin',
    'mptt',

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
    'content',
    'learning',
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_select2',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_select2_cache',
    }
}
SELECT2_CACHE_BACKEND = "select2"

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


LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.User'

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
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = '解字 Solved Chinese<noreply@solvedchinese.org>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# overwrite with local secret setting
try:
    from jiezi_secret.secret import *
except (ModuleNotFoundError, ImportError, AttributeError):
    pass
