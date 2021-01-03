import os
import re

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from jiezi.settings import BASE_DIR
from content.models.general_content_model import validate_chinese_character_or_x


class Command(BaseCommand):
    def handle(self, *args, **options):
        word_re = re.compile(r'(.*?) \[(.*?)\] /(.*?)/')
        for index in range(40):
            level_index = index // 20 + 1
            part_index = (index % 20) // 10 + 1
            lesson_index = (index % 20) + 1
            path = os.path.join(BASE_DIR, f"content/data/IC/"
                f"icl{level_index}p{part_index}_{lesson_index:02d}.txt")
            with open(path, 'r') as text_file:
                words = word_re.findall(text_file.read())
            for chinese, pinyin, definitions in words:
                try:
                    validate_chinese_character_or_x(chinese)
                except ValidationError:
                    print(f"{index}: {chinese} /{pinyin}/ ({definitions})")
