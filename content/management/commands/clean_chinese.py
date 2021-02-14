from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from content.utils import validate_chinese_character_or_x
from content.models import Radical, Character, Word


models = [Radical, Character, Word]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in models:
            for obj in model.objects.all():
                try:
                    validate_chinese_character_or_x(obj.chinese)
                except ValidationError:
                    print(repr(obj))
                    print(obj.delete())
