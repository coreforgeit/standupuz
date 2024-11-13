import typing as t
import sqlalchemy as sa
from random import randint

from .base import METADATA, begin_connection


class OptionRow(t.Protocol):
    id: int
    event_id: int
    name: str
    empty_place: int
    all_place: int
    cell: str
    price: int


OptionTable: sa.Table = sa.Table(
    "options",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('event_id', sa.Integer),
    sa.Column('name', sa.String(255)),
    sa.Column('empty_place', sa.Integer),
    sa.Column('all_place', sa.Integer),
    sa.Column('cell', sa.String(255)),
    sa.Column('price', sa.Integer)
)


async def add_option(
        event_id: int,
        title: str,
        empty_place: int,
        all_place: int,
        cell: str,
        price: int = None,
) -> None:
    query = OptionTable.insert().values(
        event_id=event_id,
        name=title,
        empty_place=empty_place,
        all_place=all_place,
        cell=cell,
        price=price
    )
    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает опции ивента
async def get_options(event_id: int) -> tuple[OptionRow]:
    query = OptionTable.select().where(OptionTable.c.event_id == event_id)
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# возвращает опцию
async def get_option(option_id: int) -> OptionRow:
    query = OptionTable.select().where(OptionTable.c.id == option_id)
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.first()


# обновляет опцию
async def update_option(
        option_id: int,
        edit_place: int = None,
        title: str = None,
        empty_place: int = None,
        all_place: int = None,
        cell: str = None
) -> None:
    query = OptionTable.update().where(OptionTable.c.id == option_id)

    if edit_place:
        query = query.values(empty_place=OptionTable.c.empty_place + edit_place)
    if title:
        query = query.values(name=title)
    if empty_place:
        query = query.values(empty_place=empty_place)
    if all_place:
        query = query.values(all_place=all_place)
    if title:
        query = query.values(cell=cell)

    async with begin_connection() as conn:
        await conn.execute(query)


# удаляет опции ивента
async def del_options(event_id: int) -> None:
    query = OptionTable.delete().where(OptionTable.c.event_id == event_id)
    async with begin_connection() as conn:
        await conn.execute(query)
