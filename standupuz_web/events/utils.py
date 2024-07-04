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


# обработка текста
def add_tags(text: str, entities: list[str]) -> str:
    if len(entities) > 1:
        entities.reverse()
    # logging.warning('^^^^')
    club = None

    for entity_str in entities:
        # logging.warning(entity_str)
        # logging.warning(type(entity_str))
        # entity = json.loads(entity_str)
        # logging.warning(type(entity))
        try:
            entity: dict = json.loads(entity_str)

            start = entity['offset']
            emoji_count = emoji.emoji_count(text[:start])
            start -= emoji_count
            end = start + entity['length']

            length = len(text)



            # tags = tags_dict.get(entity['type'])
            # logging.warning(tags)
            # if tags:
            #     text = f'{text[:end]}{tags[1]}{text[end:]}'
            #     text = f'{text[:start]}{tags[0]}{text[start:]}'
            #
            # elif entity['type'] == 'text_link':
            #     tl_text = text[start:end]
            #     tl_text0 = text[start:end]
            #     logging.warning(tl_text)


        except:
            pass

    return text.replace('\n', '<br>')