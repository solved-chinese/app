from django.core.management.base import BaseCommand
from django.utils import timezone


from accounts.models import User


DEFAULT_KEEP_SECONDS = 3600


class Command(BaseCommand):
    def handle(self, *args, **options):
        keep_time = timezone.now() - \
                    timezone.timedelta(seconds=DEFAULT_KEEP_SECONDS)
        result = User.objects.filter(is_guest=True, last_login__lt=keep_time).\
            delete()
        self.stdout.write(f"delete guest users with result {result}")
