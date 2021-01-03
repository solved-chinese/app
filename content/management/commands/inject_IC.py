import os
import re
from tqdm import tqdm
import json

from django.core.management.base import BaseCommand

from jiezi.settings import BASE_DIR
from content.models import Word, DefinitionInWord, WordSet


class Command(BaseCommand):
    def handle(self, *args, **options):
        word_re = re.compile(r'(.*?) \[(.*?)\] /(.*?)/')
        for index in tqdm(range(40)):
            level_index = index // 20 + 1
            part_index = (index % 20) // 10 + 1
            lesson_index = (index % 20) + 1
            wordset_name = f"IC Lv.{level_index} Pt.{part_index} Lesson {lesson_index}"
            if WordSet.objects.filter(name=wordset_name).exists():
                print(f'skip {wordset_name} as it exists')
                continue
            wordset = WordSet.objects.create(name=wordset_name)

            path = os.path.join(BASE_DIR, f"content/data/IC/"
                f"icl{level_index}p{part_index}_{lesson_index:02d}.txt")
            with open(path, 'r') as text_file:
                words = word_re.findall(text_file.read())

            word_objects = []
            for chinese, pinyin, definitions in words:
                assert Word.objects.filter(chinese=chinese).count() <= 1
                archive = {
                    'chinese': chinese,
                    'pinyin': pinyin,
                    'definition': definitions
                }
                archive = json.dumps(archive, ensure_ascii=False, indent=4)
                word = Word.objects.update_or_create(
                    chinese=chinese,
                    defaults={'pinyin': pinyin, 'archive': archive}
                )[0]
                if word.definitions.exists():
                    word.add_warning("There are already definitions so IC "
                        "definitions were not injected. Please verify")
                    word.save()
                else:
                    DefinitionInWord.objects.create(word=word,
                                                    definition=definitions)
                word_objects.append(word)
            wordset.words.set(word_objects)
