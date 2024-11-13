from datetime import datetime
import typing as t
import sqlalchemy as sa

from .base import METADATA, begin_connection


class OrderRow(t.Protocol):
    id: int
    created_at: datetime
    user_id: int
    phone: str
    event_id: int
    page_id: int
    option: str
    count_place: int
    in_table: bool


OrderTable: sa.Table = sa.Table(
    "orders",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime(timezone=True)),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('phone', sa.String(255)),
    sa.Column('event_id', sa.Integer),
    sa.Column('page_id', sa.BigInteger),
    sa.Column('option_name', sa.String(255)),
    sa.Column('count_place', sa.Integer),
    sa.Column('in_table', sa.Boolean, default=False),
)


# записывает новый заказ
async def add_order(user_id: int, phone: str, event_id: int, option: str, count_place: int, page_id: int) -> int:
    query = OrderTable.insert().values(
        user_id=user_id,
        phone=phone,
        event_id=event_id,
        option_name=option,
        count_place=count_place,
        page_id=page_id
    )
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.inserted_primary_key[0]


# обновляет заказ
async def update_order(order_id: int, in_google: bool = None) -> None:
    query = OrderTable.update().where(OrderTable.c.id == order_id)

    if in_google is not None:
        query = query.values(in_table=in_google)
    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает список пользователей
async def get_users_for_mailing(event_list: list[int]) -> tuple[OrderRow]:
    query = OrderTable.select().where(OrderTable.c.event_id.in_(event_list))
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()
