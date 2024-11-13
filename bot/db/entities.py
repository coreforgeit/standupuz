import typing as t
import sqlalchemy as sa

from .base import METADATA, begin_connection


class EntityRow(t.Protocol):
    id: int
    event_id: int
    type_entity: str
    offset: int
    length: int
    user: str
    url: str
    language: str
    custom_emoji_id: str


EntityTable: sa.Table = sa.Table(
    "entities",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('event_id', sa.Integer),
    sa.Column('type_entity', sa.String(255)),
    sa.Column('offset', sa.Integer()),
    sa.Column('length', sa.Integer()),
    sa.Column('url', sa.String(255)),
    sa.Column('user', sa.String(255)),
    sa.Column('language', sa.String(255)),
    sa.Column('custom_emoji_id', sa.String(255)),

)


async def add_entity(
        event_id: int,
        type_entity: str,
        offset: int = None,
        length: int = None,
        url: str = None,
        user: str = None,
        language: str = None,
        custom_emoji_id: str = None,
) -> None:
    query = EntityTable.insert().values(
        event_id=event_id,
        type_entity=type_entity,
        offset=offset,
        length=length,
        url=url,
        user=user,
        language=language,
        custom_emoji_id=custom_emoji_id,
    )
    async with begin_connection() as conn:
        await conn.execute(query)


async def get_entities(event_id: int,) -> tuple[EntityRow]:
    query = EntityTable.select().where(EntityTable.c.event_id == event_id)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()


async def delete_entities(event_id: int,) -> None:
    query = EntityTable.delete().where(EntityTable.c.event_id == event_id)
    async with begin_connection() as conn:
        await conn.execute(query)
