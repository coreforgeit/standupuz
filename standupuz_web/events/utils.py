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
    # if len(entities) > 1:
    #     entities.reverse()
    logging.warning('^^^^')
    logging.warning(f'{type(entities)} {len(entities)}')
    logging.warning(entities)

    # logging.warning(entities)
    # entities.reverse()
    # logging.warning(entities)
    for entity_str in entities:
        logging.warning(entity_str)
    #     try:
    #         logging.warning(entity_str)
    #         entity = json.loads(entity_str)
    #
    #         start = entity['offset']
    #
    #         emoji_count = emoji.emoji_count(text[:start])
    #         start -= emoji_count
    #         end = start + entity.length
    #
    #         tags = tags_dict.get(entity.type)
    #         if tags:
    #             # print(f'<{entity.type}> {text[start]} | {text[start:end]} {entity.offset}')
    #             text = f'{text[:end]}{tags[1]}{text[end:]}'
    #             text = f'{text[:start]}{tags[0]}{text[start:]}'
    #
    #     except:
    #         pass

    return text.replace('\n', '<br>')