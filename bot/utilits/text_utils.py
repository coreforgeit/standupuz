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
    # entities.reverse()
    # text = text.strip()
    # print(text[:2])
    print('----')
    print(text)

    for entity in entities:
        start = entity.offset
        end = entity.offset + entity.length + 1
        tags = tags_dict.get(entity.type)
        if tags:
            print(f'<{entity.type}> {text[start]} {text[start:end]} {entity.offset}')
    #         text = f'{text[:end]}{tags[1]}{text[end:]}'
    #         text = f'{text[:start]}{tags[0]}{text[start:]}'
            # break


        # if entity.type == MessageEntityType.BOLD:
        #     text = f'{text[:end]}</b>{text[end:]}'
        #     text = f'{text[:start]}<b>{text[start:]}'
        # elif entity.type == MessageEntityType.ITALIC:
        #     text = f'{text[:end]}</i>{text[end:]}'
        #     text = f'{text[:start]}<i>{text[start:]}'

    return text #  .replace('\n', '<br>')
