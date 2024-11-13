import logging
import os
import emoji
import json

from standupuz_web.settings import MEDIA_ROOT
from .bot import download_file
from .data import tags_dict


# возвращает путь вк фото
def get_photo_url(photo_id: str) -> str:
    path = os.path.join(MEDIA_ROOT, f'{photo_id}.jpg')
    if not os.path.exists(path):
        download_file(photo_id, path)
    return f'../media/{photo_id}.jpg'


# возвращает путь вк фото
def get_photo_url_mob(photo_id: str) -> str:
    path = os.path.join(MEDIA_ROOT, f'{photo_id}.jpg')
    if not os.path.exists(path):
        download_file(photo_id, path)
    return f'/media/{photo_id}.jpg'
