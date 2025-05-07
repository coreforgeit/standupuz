import sqlalchemy as sa
import typing as t
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, begin_connection


class Option(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    empty_place: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    all_place: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    cell: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    price: Mapped[int] = mapped_column(sa.Integer, nullable=True)

    @classmethod
    async def add_option(
        cls,
        event_id: int,
        name: str,
        empty_place: int,
        all_place: int,
        cell: str,
        price: int = None,
    ) -> None:
        stmt = sa.insert(cls).values(
            event_id=event_id,
            name=name,
            empty_place=empty_place,
            all_place=all_place,
            cell=cell,
            price=price,
        )
        async with begin_connection() as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def get_options(cls, event_id: int) -> list[t.Self]:
        stmt = sa.select(cls).where(cls.event_id == event_id)
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
        return result.all()

    @classmethod
    async def get_option(cls, option_id: int) -> t.Optional[t.Self]:
        stmt = sa.select(cls).where(cls.id == option_id)
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
        return result.first()

    @classmethod
    async def update_option(
        cls,
        option_id: int,
        edit_place: int = None,
        name: str = None,
        empty_place: int = None,
        all_place: int = None,
        cell: str = None
    ) -> None:
        stmt = sa.update(cls).where(cls.id == option_id)

        if edit_place is not None:
            stmt = stmt.values(empty_place=cls.empty_place + edit_place)
        if name is not None:
            stmt = stmt.values(name=name)
        if empty_place is not None:
            stmt = stmt.values(empty_place=empty_place)
        if all_place is not None:
            stmt = stmt.values(all_place=all_place)
        if cell is not None:
            stmt = stmt.values(cell=cell)

        async with begin_connection() as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def del_options(cls, event_id: int) -> None:
        stmt = sa.delete(cls).where(cls.event_id == event_id)
        async with begin_connection() as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def old_data_insert(cls) -> None:
        """
        Reads old data from db/old_data/orders.csv (with header),
        remaps event_id using db/old_data/id_map.json,
        and bulk-inserts all rows into the orders table.
        """
        import csv
        import json
        from pathlib import Path
        import sqlalchemy as sa
        from datetime import datetime

        data_dir = Path("db") / "old_data"
        csv_path = data_dir / f"{cls.__tablename__}.csv"
        map_path = data_dir / "id_map.json"
        if not csv_path.exists() or not map_path.exists():
            return

        # load mapping of old event_id to new event_id
        with map_path.open(encoding="utf-8") as mf:
            raw_map = json.load(mf)
        id_map = {int(k): v for k, v in raw_map.items()}

        # read CSV rows
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        async with begin_connection() as conn:
            for row in rows:
                # parse created_at, treating 'NULL' as absent
                created_at_str = row.get("created_at")
                if created_at_str and created_at_str.upper() != "NULL":
                    created_at = datetime.fromisoformat(created_at_str)
                else:
                    created_at = None

                old_event = int(row["event_id"]) if row.get("event_id") else None
                new_event = id_map.get(old_event, old_event)

                data = {
                    "id": int(row["id"]),
                    "created_at": created_at,
                    "user_id": int(row["user_id"]) if row.get("user_id") else None,
                    "phone": row.get("phone"),
                    "event_id": new_event,
                    "page_id": int(row["page_id"]) if row.get("page_id") else None,
                    "option_name": row.get("option_name"),
                    "count_place": int(row["count_place"]) if row.get("count_place") else None,
                    "in_table": row.get("in_table") == "True",
                }
                stmt = sa.insert(cls).values(**data)
                await conn.execute(stmt)
            await conn.commit()
