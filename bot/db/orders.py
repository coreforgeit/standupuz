import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import typing as t

from .base import Base, begin_connection


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=True)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    phone: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    event_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    page_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    option: Mapped[str] = mapped_column("option_name", sa.String(255), nullable=False)
    count_place: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    in_table: Mapped[bool] = mapped_column(sa.Boolean(), nullable=False, default=False)

    @classmethod
    async def add_order(
        cls,
        user_id: int,
        phone: str,
        event_id: int,
        option: str,
        count_place: int,
        page_id: int,
    ) -> int:
        now = datetime.utcnow()
        stmt = sa.insert(cls).values(
            created_at=now,
            user_id=user_id,
            phone=phone,
            event_id=event_id,
            option_name=option,
            count_place=count_place,
            page_id=page_id,
            in_table=False,
        )
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
            await conn.commit()
            return result.inserted_primary_key[0]

    @classmethod
    async def update_order(
        cls,
        order_id: int,
        in_google: bool = None,
    ) -> None:
        stmt = sa.update(cls).where(cls.id == order_id)
        if in_google is not None:
            stmt = stmt.values(in_table=in_google)
        async with begin_connection() as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def get_users_for_mailing(
        cls,
        event_list: list[int],
    ) -> list[t.Self]:
        stmt = sa.select(cls).where(cls.event_id.in_(event_list))
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
        return result.scalars().all()

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
                old_event = int(row["event_id"]) if row.get("event_id") else None
                new_event = id_map.get(old_event, old_event)
                data = {
                    # "id": int(row["id"]),
                    "created_at": datetime.now(),
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

