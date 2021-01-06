from tqdm import tqdm

from django.core.management.base import BaseCommand

from content.models import Character, DefinitionInCharacter, Radical
from content.data.makemeahanzi_dictionary import get_makemeahanzi_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        for character in tqdm(Character.objects.all()):
            character.fill_makemeahanzi_data()
            character.save()
        for radical in tqdm(Radical.objects.all()):
            radical.fill_makemeahanzi_data()
            radical.save()
