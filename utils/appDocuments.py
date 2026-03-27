import json
import os

from django.conf import settings


def get_ipem_data_json():
    # Getting data in ipem-data.json
    json_path = settings.BASE_DIR / 'appDocuments/ipem-data.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        form_data = json.load(file)

    return form_data


def get_imgs_path():
    # Verifying if images exist
    imgs = ['brasao', 'convenio']
    imgs_path = {}

    for img in imgs:
        if os.path.exists(settings.MEDIA_ROOT + f'{img}.png'):
            imgs_path[img] = settings.MEDIA_ROOT + f'{img}.png'
        else:
            imgs_path[img] = None

    return imgs_path
