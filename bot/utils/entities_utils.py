from aiogram.types import MessageEntity

import typing as t
import json


# подготавливает сущности к сохранению (превращает в список строк)
# type='bold' offset=58 length=53 url=None user=None language=None custom_emoji_id=None (30.01.2025)
def save_entities(entities: t.Optional[list[MessageEntity]]) -> str:
    entities_list = []
    if entities:
        for entity in entities:
            entity_dict = entity.dict()
            entities_list.append(entity_dict)

    return json.dumps(entities_list)


# восстанавливает сущности
def recover_entities(entities_str: t.Optional[str]) -> list[MessageEntity]:
    if not entities_str:
        return []

    entities_list = []
    entities: list[dict] = json.loads(entities_str)
    if entities:
        for entity in entities:
            entities_list.append(MessageEntity(**entity))

    return entities_list
