from django.core.management import call_command
from celery import shared_task

@shared_task
def clear_guests():
    call_command('clear_guests')
