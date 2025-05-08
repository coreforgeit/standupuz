import logging
import os
import emoji
import json

from standupuz_web.settings import MEDIA_ROOT
from .bot import download_file
from .data import tags_dict


# возвращает путь вк фото
def get_photo_url(photo_id: str) -> str:
    path = os.path.join(MEDIA_ROOT, f'{1}.jpg')
    if not os.path.exists(path):
        download_file(1, path)
    return f'../media/{1}.jpg'


# возвращает путь вк фото
def get_photo_url_mob(photo_id: str) -> str:
    path = os.path.join(MEDIA_ROOT, f'{1}.jpg')
    if not os.path.exists(path):
        download_file(1, path)
    return f'/media/{1}.jpg'
