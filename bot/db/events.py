from datetime import datetime, date, time
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql

from .base import METADATA, begin_connection
from config import Config
from init import log_error


class EventRow(t.Protocol):
    id: int
    created_at: datetime
    title: str
    event_date: date
    event_time: time
    text: str
    entities: list[str]
    photo_id: str
    is_active: bool
    page_id: int
    text_1: str
    text_2: str
    text_3: str
    text_site: str


class PopTimeRow(t.Protocol):
    event_time: time
    count_time: int


EventTable: sa.Table = sa.Table(
    "events",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime(timezone=True)),
    sa.Column('title', sa.String(255)),
    sa.Column('club', sa.String(255)),
    sa.Column('event_date', sa.Date()),
    sa.Column('event_time', sa.Time()),
    sa.Column('text', sa.Text()),
    sa.Column('entities', sa_postgresql.ARRAY(sa.String(255))),
    sa.Column('photo_id', sa.String(255)),
    sa.Column('is_active', sa.Boolean()),
    sa.Column('page_id', sa.Integer),
    sa.Column('text_1', sa.Text()),
    sa.Column('text_2', sa.Text()),
    sa.Column('text_3', sa.Text()),
    # sa.Column('text_site', sa.Text()),
)


async def add_event(
        title: str,
        event_date: date,
        event_time: time,
        text: str,
        club: str,
        # entities: list[str],
        photo_id: str,
        is_active: bool,
        page_id: int,
        text_1: str = None,
        text_2: str = None,
        text_3: str = None
) -> int:
    now = datetime.now(Config.tz)
    query = EventTable.insert().values(
        created_at=now,
        title=title,
        club=club,
        event_date=event_date,
        event_time=event_time,
        text=text,
        # entities=entities,
        photo_id=photo_id,
        is_active=is_active,
        page_id=page_id,
        text_1=text_1,
        text_2=text_2,
        text_3=text_3,
        # text_site=text_site,
    )
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.inserted_primary_key[0]


#  db.update_event (
#                     is_active=is_active,
#                     title=title,
#                     date=event_date_str,
#                     time=event_time_str,
#                     page_id=table.id)
# обновляет данные ивента
async def update_event(
        event_id: int = None,
        page_id: int = None,
        title: str = None,
        new_date: date = None,
        new_time: time = None,
        photo_id: str = None,
        text: str = None,
        entities: list[str] = None,
        text_1: str = None,
        text_2: str = None,
        text_3: str = None,
        is_active: bool = None
) -> None:
    query = EventTable.update()

    if event_id:
        query = query.where(EventTable.c.id == event_id)
    elif page_id:
        query = query.where(EventTable.c.page_id == page_id)

    if title:
        query = query.values(title=title)
    if new_date:
        query = query.values(event_date=new_date)
    if new_time:
        query = query.values(event_time=new_time)
    if photo_id:
        query = query.values(photo_id=photo_id)
    if text:
        query = query.values(text=text)
    if entities:
        query = query.values(entities=entities)
    if text_1:
        query = query.values(text_1=text_1)
    if text_2:
        query = query.values(text_2=text_2)
    if text_3:
        query = query.values(text_3=text_3)
    if is_active is not None:
        query = query.values(is_active=is_active)
    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает ивенты
async def get_events(active: bool = False, last_10: bool = False) -> tuple[EventRow]:
    # query = EventTable.select().order_by(sa.desc(EventTable.c.created_at))
    query = EventTable.select()

    if active:
        query = query.where(EventTable.c.is_active).order_by(EventTable.c.event_date)
    if last_10:
        # query = query.limit(10).order_by(EventTable.c.event_date)
        query = query.limit(10).order_by(sa.desc(EventTable.c.event_date))
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# возвращает ивент
async def get_event(event_id: int = None, page_id: int = None) -> EventRow:
    query = EventTable.select().where(EventTable.c.id == event_id)
    if event_id:
        query = query.where(EventTable.c.id == event_id)
    elif page_id:
        query = EventTable.select().where(EventTable.c.page_id == page_id)
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.first()


# популярные варианты времени
async def get_popular_time_list() -> tuple[PopTimeRow]:
    query = (EventTable.select().with_only_columns(
        EventTable.c.event_time,
        sa.func.count(EventTable.c.id).label('count_time')).
             group_by(EventTable.c.event_time).order_by(sa.func.count(EventTable.c.id)).limit(6)
             )
    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# закрывает старые ивенты
async def close_old_events() -> None:
    now = datetime.now(Config.tz)
    query = EventTable.update().where(EventTable.c.event_date < now.date()).values(is_active=False)
    async with begin_connection() as conn:
        await conn.execute(query)
