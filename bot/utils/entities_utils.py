from aiogram.types import MessageEntity

import typing as t
import db


# подготавливает сущности к сохранению (превращает в список строк)
async def save_entities(event_id: int, entities: t.Optional[list[MessageEntity]]) -> None:
    if entities:
        for entity in entities:
            await db.add_entity(
                event_id=event_id,
                type_entity=entity.type,
                offset=entity.offset,
                length=entity.length,
                url=entity.url,
                user=entity.user,
                language=entity.language,
                custom_emoji_id=entity.custom_emoji_id
            )


# восстанавливает сущности
async def recover_entities(event_id: int) -> list[MessageEntity]:
    entities = await db.get_entities(event_id)
    entities_list = []
    if entities:
        for entity in entities:
            entities_list.append(MessageEntity(
                type=entity.type_entity,
                offset=entity.offset,
                length=entity.length,
                url=entity.url,
                user=None,
                language=entity.language,
                custom_emoji_id=entity.custom_emoji_id
            ))
    return entities_list
