import os
import re
from tqdm import tqdm
import json

from django.core.management.base import BaseCommand

from jiezi.settings import BASE_DIR
from content.models import Word, DefinitionInWord


class Command(BaseCommand):
    def handle(self, *args, **options):
        for word in Word.objects.all():
            if word.definitions.count() == 1:
                definition = word.definitions.get()
                definitions = definition.definition.split(';')
                if len(definitions) > 1:
                    definition.definition = definitions[0].strip()
                    definition.save()
                    print(f"change {word} to {definitions}")
                for index in range(1, len(definitions)):
                    DefinitionInWord.objects.create(
                        word=word, order=index,
                        definition=definitions[index].strip())
