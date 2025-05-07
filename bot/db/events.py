import os.path

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy.dialects.postgresql as sa_postgresql
from datetime import datetime, date, time
import typing as t

from .base import Base, begin_connection
from settings.config import Config
from settings import log_error


class PopTimeRow(t.Protocol):
    event_time: time
    count_time: int


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=True)
    title: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    club: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    event_date: Mapped[date] = mapped_column(sa.Date(), nullable=True)
    event_time: Mapped[time] = mapped_column(sa.Time(), nullable=True)
    text: Mapped[str] = mapped_column(sa.Text(), nullable=True)
    entities: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    photo_id: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(sa.Boolean(), nullable=True)
    page_id: Mapped[int] = mapped_column(sa.Integer(), nullable=True)
    text_1: Mapped[str] = mapped_column(sa.Text(), nullable=True)
    text_2: Mapped[str] = mapped_column(sa.Text(), nullable=True)
    text_3: Mapped[str] = mapped_column(sa.Text(), nullable=True)
    ticket_url: Mapped[str] = mapped_column(sa.Text(), nullable=True)

    @classmethod
    async def add_event(
            cls,
            title: str,
            event_date: date,
            event_time: time,
            text: str,
            club: str,
            photo_id: str,
            ticket_url: str,
            is_active: bool,
            page_id: int,
            entities: str = None,
            text_1: str = None,
            text_2: str = None,
            text_3: str = None,
    ) -> int:
        now = datetime.now(Config.tz)
        stmt = sa.insert(cls).values(
            created_at=now,
            title=title,
            club=club,
            event_date=event_date,
            event_time=event_time,
            text=text,
            entities=entities,
            photo_id=photo_id,
            is_active=is_active,
            page_id=page_id,
            text_1=text_1,
            text_2=text_2,
            text_3=text_3,
            ticket_url=ticket_url,
        )
        async with begin_connection() as conn:
            try:
                result = await conn.execute(stmt)
                await conn.commit()
                return result.inserted_primary_key[0]
            except Exception as e:
                log_error(f"add_event failed: {e}")
                raise

    @classmethod
    async def update_event(
        cls,
        event_id: int = None,
        page_id: int = None,
        title: str = None,
        new_date: date = None,
        new_time: time = None,
        photo_id: str = None,
        text: str = None,
        entities: str = None,
        text_1: str = None,
        text_2: str = None,
        text_3: str = None,
        ticket_url: str = None,
        is_active: bool = None,
    ) -> None:
        stmt = sa.update(cls)
        if event_id is not None:
            stmt = stmt.where(cls.id == event_id)
        elif page_id is not None:
            stmt = stmt.where(cls.page_id == page_id)

        # apply each update directly
        if title:
            stmt = stmt.values(title=title)
        if new_date:
            stmt = stmt.values(event_date=new_date)
        if new_time:
            stmt = stmt.values(event_time=new_time)
        if photo_id:
            stmt = stmt.values(photo_id=photo_id)
        if text:
            stmt = stmt.values(text=text)
        if entities:
            stmt = stmt.values(entities=entities)
        if text_1:
            stmt = stmt.values(text_1=text_1)
        if text_2:
            stmt = stmt.values(text_2=text_2)
        if text_3:
            stmt = stmt.values(text_3=text_3)
        if ticket_url:
            stmt = stmt.values(ticket_url=ticket_url)
        if is_active is not None:
            stmt = stmt.values(is_active=is_active)

        async with begin_connection() as conn:
            try:
                await conn.execute(stmt)
                await conn.commit()
            except Exception as e:
                log_error(f"update_event failed: {e}")
                raise

    @classmethod
    async def get_events(cls, active: bool = False, last_10: bool = False) -> list[t.Self]:
        stmt = sa.select(cls)
        if active:
            stmt = stmt.where(cls.is_active).order_by(cls.event_date)
        if last_10:
            stmt = stmt.limit(10).order_by(sa.desc(cls.event_date))
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
        return result.all()

    @classmethod
    async def get_event(cls, event_id: int = None, page_id: int = None) -> t.Optional[t.Self]:
        if event_id is not None:
            stmt = sa.select(cls).where(cls.id == event_id)
        elif page_id is not None:
            stmt = sa.select(cls).where(cls.page_id == page_id)
        else:
            return None
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_popular_time_list(cls) -> list[PopTimeRow]:
        stmt = (
            sa.select(cls.event_time, sa.func.count(cls.id).label("count_time"))
            .group_by(cls.event_time)
            .order_by(sa.func.count(cls.id))
            .limit(6)
        )
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
        return result.all()

    @classmethod
    async def close_old_events(cls) -> None:
        now = datetime.now(Config.tz)
        stmt = sa.update(cls).where(cls.event_date < now.date()).values(is_active=False)
        async with begin_connection() as conn:
            try:
                await conn.execute(stmt)
                await conn.commit()
            except Exception as e:
                log_error(f"close_old_events failed: {e}")
                raise

    @classmethod
    async def old_data_insert(cls) -> None:
        """
        Reads old data from old_data/events.csv (with header),
        bulk-inserts all rows into the events table,
        and writes a JSON file mapping old IDs to new IDs in old_data/events_id_map.json.
        """
        import csv
        import json
        from pathlib import Path
        import sqlalchemy as sa
        from datetime import datetime, date, time

        data_dir = Path("db/old_data")
        # csv_path = os.path.join(data_dir, f"{cls.__tablename__}.csv")
        csv_path = data_dir / f"{cls.__tablename__}.csv"

        print(f'csv_path: {csv_path} {os.path.exists(csv_path)}')
        if not os.path.exists(csv_path):
            return

        # read all old rows
        with csv_path.open(newline="", encoding="utf-8") as f:
        # with open(csv_path, "w", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        id_map: dict[int, int] = {}
        print(len(rows))

        async with begin_connection() as conn:
            for row in rows:
                print(row["id"])
                old_id = int(row["id"])
                stmt = sa.insert(cls).values(
                    created_at=(datetime.fromisoformat(row["created_at"])
                                if row.get("created_at") else None),
                    title=row.get("title"),
                    club=row.get("club"),
                    event_date=(date.fromisoformat(row["event_date"])
                                if row.get("event_date") else None),
                    event_time=(time.fromisoformat(row["event_time"])
                                if row.get("event_time") else None),
                    text=row.get("text"),
                    entities=None,
                    photo_id=row.get("photo_id"),
                    is_active=(row.get("is_active") == "True"),
                    page_id=(int(row["page_id"]) if row.get("page_id") else None),
                    text_1=row.get("text_1"),
                    text_2=row.get("text_2"),
                    text_3=row.get("text_3"),
                    ticket_url=row.get("ticket_url"),
                )
                result = await conn.execute(stmt)
                # capture new primary key
                new_id = result.inserted_primary_key[0]
                id_map[old_id] = new_id

                # await conn.execute(stmt)

                await conn.commit()

        # write the mapping of old IDs to new IDs
        # map_path = os.path.join(data_dir, f"id_map.json")
        map_path = data_dir / f"id_map.json"

        with open(map_path, "w", encoding="utf-8") as mf:
            json.dump(id_map, mf, ensure_ascii=False, indent=2)

