import json
import os

from jiezi.settings import BASE_DIR


def get_makemeahanzi_data():
    json_path = os.path.join(BASE_DIR,
                             'content/data/makemeahanzi_dictionary.json')
    with open(json_path, 'r') as json_file:
        characters_data = json.load(json_file)
    return characters_data
