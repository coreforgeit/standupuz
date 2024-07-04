import sqlite3
import os

from aiogram.types import MessageEntity


# db_path = '"D:\PycharmProjects\\other\\standupuz\\bot\\data\\data.db"'
# db_path = os.path.join('bot', 'data', 'data.db')
db_path = os.path.join('data', 'data.db')


def get_users():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    result = cur.execute('select * from users').fetchall()
    cur.close()
    return result


def get_events():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    result = cur.execute('select * from events').fetchall()
    cur.close()
    return result


def get_entities(event_id) -> list:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    results = cur.execute('select type, offset, length, url from entities where event_id = ? ',
                          (event_id,)).fetchall()
    cur.close()
    entities = []
    for result in results:
        if result[0] == 'custom_emoji':
            entity = MessageEntity(type=result[0], offset=result[1], length=result[2], custom_emoji_id=result[3])
        else:
            entity = MessageEntity(type=result[0], offset=result[1], length=result[2], url=result[3])
        entities.append(entity)

    return entities


def get_options(event_id: int):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    result = cur.execute('select * from events_options where event_id = ?', (event_id,)).fetchall()
    cur.close()
    return result
