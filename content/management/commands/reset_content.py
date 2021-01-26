from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.management import call_command
from content.models import AudioFile

class Command(BaseCommand):
    def handle(self, *args, **options):
        app_models = list(apps.get_app_config('content').get_models())
        app_models.remove(AudioFile)
        app_models.append(AudioFile)

        print("now delete all content objects")
        for model in app_models:
            print(model.objects.all().delete())
        print("now load data, please wait for about 30 seconds")
        call_command('loaddata', 'content_data.json')

