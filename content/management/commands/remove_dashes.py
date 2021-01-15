from tqdm import tqdm

from django.core.management.base import BaseCommand

from content.models import Radical


class Command(BaseCommand):
    def handle(self, *args, **options):
       print(Radical.objects.filter(pinyin='--').update(pinyin=''))
       print(Radical.objects.filter(pinyin='-').update(pinyin=''))
       print(Radical.objects.filter(definition='--').update(definition=''))
       print(Radical.objects.filter(definition='-').update(definition=''))
       print(Radical.objects.filter(explanation='--').update(explanation=''))
       print(Radical.objects.filter(explanation='-').update(explanation=''))
