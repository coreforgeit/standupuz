import logging
import os
import emoji
import json

from standupuz_web.settings import MEDIA_ROOT
from .bot import download_file
from .data import tags_dict


# возвращает путь вк фото

def get_photo_url(event_id: str) -> str:
    return f'site/photo/{event_id}.jpg'
