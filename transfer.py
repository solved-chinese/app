import pandas as pd
import os
import json

from content.models import *
from django.core.files import File


ALL_MODELS = [Radical, Character, DefinitionInCharacter, RadicalInCharacter,
              Word, DefinitionInWord, CharacterInWord, Sentence]


def process_df(df):
    df.replace('', None, inplace=True)
    df.fillna('', inplace=True)
    return df


if __name__ == '__main__':
    for model in ALL_MODELS:
        model.objects.all().delete()

    with open('Entry.xlsx', 'rb') as file:
        character_df = pd.read_excel(file, 'Characters')
        character_df = process_df(character_df)
        radical_df = pd.read_excel(file, '偏旁')
        radical_df = process_df(radical_df)

    radicals = {} # id to radical
    for i, row in radical_df.iterrows():
        if not row['id'] or not row['chinese']:
            print(f"ignore row {i}: {row} due to invalid id / chinese")
            continue

        definition = row['definition'].strip()
        definition = '' if definition == '--' else definition
        chinese = row['chinese'].strip()
        pinyin = row['pinyin'].strip()
        id = int(row['id'])
        explanation = row['mnemonic_explanation'].strip()


        if '*' in chinese:
            chinese = chinese.replace('*', '')
            if Radical.objects.filter(chinese=chinese).exists():
                radical = Radical.objects.filter(chinese=chinese).get()
            else:
                defaults = dict(
                    pinyin=pinyin,
                    explanation=explanation,
                    definition=definition
                )
                radical = Radical.objects.update_or_create(
                    chinese=chinese, defaults=defaults)[0]
        else:
            defaults = dict(
                pinyin=pinyin,
                explanation=explanation,
                definition=definition
            )
            radical = Radical.objects.update_or_create(
                chinese=chinese, defaults=defaults)[0]

        path = f'radical_mnemonic/R{id:04d}.png'
        if os.path.exists(path):
            radical.image.save(path, File(open(path, 'rb')))

        radicals[id]  = radical

    print('----------------')
    print('start characters')
    print('----------------')

    for i, row in character_df.iterrows():
        if not row['id'] or not row['chinese']:
            print(f"ignore row {i}: {row} due to invalid id / chinese")
            continue

        chinese = row['chinese'].strip()
        pinyin = row['pinyin'].strip()
        memory_aid = row['mnemonic_explanation'].strip()

        d = {}
        d['structure'] = row['structure']
        d['is_preview_definition'] = row['is_preview_definition']
        d['is_preview_pinyin'] = row['is_preview_pinyin']

        character = Character.objects.update_or_create(
            chinese=chinese,
            defaults=dict(pinyin=pinyin, memory_aid=memory_aid,
                          archive=json.dumps(d))
        )[0]

        # def starts
        for j in range(1, 4):
            field = f"definition_{j}"
            definition = row[field].strip()
            if definition:
                DefinitionInCharacter.objects.get_or_create(
                    definition=definition, character=character, order=j)
            else:
                break

        # radicals start
        for j in range(1, 4):
            field = f"radical_{j}"
            radical_id = row[field]
            if radical_id:
                try:
                    radical_id = int(radical_id)
                except ValueError:
                    continue
                radical = radicals.get(radical_id, None)
                if radical is None:
                    continue
                RadicalInCharacter.objects.get_or_create(
                    character=character, radical=radical, order=j)
            else:
                break

    print('----------------')
    print('start words')
    print('----------------')

    for i, row in character_df.iterrows():
        # words start
        for j in range(1, 3):
            word_name = f"example_{j}_word"
            pinyin_name = f"example_{j}_pinyin"
            if not row[word_name] or not row[pinyin_name]:
                continue
            word = row[word_name].strip()
            if len(word) > 5:
                continue
            pinyin = row[pinyin_name].strip()
            Word.objects.get_or_create(chinese=word,
                                       defaults={'pinyin': pinyin})
