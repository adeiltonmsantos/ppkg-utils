import os

from django.conf import settings


def get_imgs_path():
    # Verifying if images exist
    imgs = ['brasao', 'convenio']
    imgs_path = {}

    for img in imgs:
        try:
            if os.path.exists(settings.MEDIA_ROOT + f'{img}.png'):
                imgs_path[img] = settings.MEDIA_ROOT + f'{img}.png'
            else:
                imgs_path[img] = None
        except Exception:
            if os.path.exists(settings.MEDIA_ROOT / f'{img}.png'):
                imgs_path[img] = settings.MEDIA_ROOT / f'{img}.png'
            else:
                imgs_path[img] = None

    return imgs_path
