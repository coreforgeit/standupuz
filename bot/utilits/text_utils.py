from aiogram.types import MessageEntity
from aiogram.enums.message_entity_type import MessageEntityType


tags_dict = {
    MessageEntityType.BOLD.value: ['<b>', '</b>'],
    MessageEntityType.ITALIC.value: ['<i>', '</i>'],
    MessageEntityType.CODE.value: ['<code>', '</code>'],
    MessageEntityType.UNDERLINE.value: ['<u>', '</u>'],
    MessageEntityType.STRIKETHROUGH.value: ['<s>', '</u>'],
}


def add_tags(text: str, entities: list[MessageEntity]) -> str:
    entities.reverse()
    for entity in entities:
        start = entity.offset
        end = entity.offset + entity.length
        if entity.type == MessageEntityType.BOLD:
            text = f'{text[:end]}</b>{text[end:]}'
            text = f'{text[:start]}<b>{text[start:]}'
        elif entity.type == MessageEntityType.ITALIC:
            text = f'{text[:end]}</i>{text[end:]}'
            text = f'{text[:start]}<i>{text[start:]}'

