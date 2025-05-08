import sqlalchemy as sa
import typing as t
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import postgresql as psql
from datetime import datetime


from .base import Base, begin_connection


class Info(Base):
    __tablename__ = "bot_info"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    last_update: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=True)
    hello_text: Mapped[str] = mapped_column(sa.Text(), nullable=True)
    hello_entities: Mapped[list[str]] = mapped_column(psql.ARRAY(sa.String(255)), nullable=True)
    text_1: Mapped[str] = mapped_column(sa.Text(), nullable=True)
    text_2: Mapped[str] = mapped_column(sa.Text(), nullable=True)
    text_3: Mapped[str] = mapped_column(sa.Text(), nullable=True)

    @classmethod
    async def get_info(cls) -> t.Self:
        query = sa.select(cls).where(cls.id == 1)
        async with begin_connection() as conn:
            result = await conn.execute(query)
            return result.scalars().first()

    @classmethod
    async def update_info(
        cls,
        hello_text: str = None,
        hello_entities: list[str] = None,
        text_1: str = None,
        text_2: str = None,
        text_3: str = None,
    ) -> None:
        now = datetime.utcnow()
        query = sa.update(cls).where(cls.id == 1).values(last_update=now)

        if hello_text is not None:
            query = query.values(hello_text=hello_text)
        if hello_entities is not None:
            query = query.values(hello_entities=hello_entities)
        if text_1 is not None:
            query = query.values(text_1=text_1)
        if text_2 is not None:
            query = query.values(text_2=text_2)
        if text_3 is not None:
            query = query.values(text_3=text_3)

        async with begin_connection() as conn:
            await conn.execute(query)
            await conn.commit()

    @classmethod
    async def old_data_insert(cls) -> None:
        from pathlib import Path
        import csv
        """
        Reads old data from old_data/bot_info.csv (with header)
        and bulk-inserts all rows into the bot_info table.
        """
        file_path = Path('db/old_data') / f"{cls.__tablename__}.csv"
        if not file_path.exists():
            return

        with file_path.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        async with begin_connection() as conn:
            for row in rows:
                data = {
                    "id": int(row["id"]),
                    "last_update": datetime.now(),
                    "hello_text": row.get("hello_text"),
                    "hello_entities": row.get("hello_entities").split(";") if row.get("hello_entities") else None,
                    "text_1": row.get("text_1"),
                    "text_2": row.get("text_2"),
                    "text_3": row.get("text_3"),
                }
                insert_stmt = psql.insert(cls).values(**data)
                await conn.execute(insert_stmt)
            await conn.commit()
