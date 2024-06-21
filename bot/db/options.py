from datetime import datetime, date, time
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql
from utilits.entities_utils import save_entities
from random import randint

from .base import METADATA, begin_connection
from config import Config
from .sqlite_temp import get_options


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
        name: str,
        empty_place: int,
        all_place: int,
        cell: str,
        price: int,
) -> None:
    query = OptionTable.insert().values(
        event_id=event_id,
        name=name,
        empty_place=empty_place,
        all_place=all_place,
        cell=cell,
        price=price
    )
    async with begin_connection() as conn:
        await conn.execute(query)


async def add_options():
    time_start = datetime.now()
    options = get_options()
    for option in options:
        if option[1] > 136:
            print(option)
            await add_option(
                event_id=option[1],
                name=option[2],
                empty_place=option[3],
                all_place=option[4],
                cell=option[5],
                price=randint(1, 10) * 10000
            )

    print(datetime.now() - time_start)