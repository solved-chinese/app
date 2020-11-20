# https://eeinte.ch/stream/progress-bar-django-using-celery/
# https://github.com/czue/celery-progress

from __future__ import absolute_import, unicode_literals
# Django settings
import os
from django.conf import settings
# Celery app
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jiezi.settings')

app = Celery('jiezi', broker='redis://localhost')

# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear_guests': { # clear guest account once every hour
        'task': 'accounts.tasks.clear_guests',
        'schedule': 3600.0,
    },
}
