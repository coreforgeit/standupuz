import typing as t
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql
from .base import METADATA, begin_connection

from datetime import datetime


class InfoRow(t.Protocol):
    id: int
    last_update: datetime
    hello_text: str
    hello_entities: list[str]
    text_1: str
    text_2: str
    text_3: str


InfoTable: sa.Table = sa.Table(
    "bot_info",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('last_update', sa.DateTime(timezone=True)),
    sa.Column('hello_text', sa.Text()),
    sa.Column('hello_entities', psql.ARRAY(sa.String(255))),
    sa.Column('text_1', sa.Text()),
    sa.Column('text_2', sa.Text()),
    sa.Column('text_3', sa.Text()),
)


# возвращает инфо
async def get_info() -> InfoRow:
    query = InfoTable.select().where(InfoTable.c.id == 1)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.first()


# обновляет данные
async def update_info(
        hello_text: str = None,
        hello_entities: list = None,
        text_1: str = None,
        text_2: str = None,
        text_3: str = None,
) -> None:
    query = InfoTable.update().where(InfoTable.c.id == 1)
    if hello_text:
        query = query.values(hello_text=hello_text)

    if text_1:
        query = query.values(text_1=text_1)
    if text_2:
        query = query.values(text_2=text_2)
    if text_3:
        query = query.values(text_3=text_3)

    async with begin_connection() as conn:
        await conn.execute(query)
