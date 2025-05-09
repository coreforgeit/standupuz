import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, begin_connection


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    type_entity: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    offset: Mapped[int] = mapped_column(sa.Integer, nullable=True)
    length: Mapped[int] = mapped_column(sa.Integer, nullable=True)
    url: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    user: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    language: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    custom_emoji_id: Mapped[str] = mapped_column(sa.String(255), nullable=True)

    @classmethod
    async def add_entity(
        cls,
        event_id: int,
        type_entity: str,
        offset: int = None,
        length: int = None,
        url: str = None,
        user: str = None,
        language: str = None,
        custom_emoji_id: str = None,
    ) -> None:
        stmt = sa.insert(cls).values(
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
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def get_entities(cls, event_id: int) -> list[tuple]:
        stmt = sa.select(cls).where(cls.event_id == event_id)
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
            return result.all()

    @classmethod
    async def delete_entities(cls, event_id: int) -> None:
        stmt = sa.delete(cls).where(cls.event_id == event_id)
        async with begin_connection() as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def old_data_insert(cls) -> None:
        """
        Читает CSV из old_data/entities.csv (с заголовком)
        и вставляет все строки в таблицу entities.
        """
        import csv
        from pathlib import Path
        import sqlalchemy as sa

        file_path = Path("old_data") / f"{cls.__tablename__}.csv"
        if not file_path.exists():
            return

        with file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        async with begin_connection() as conn:
            for row in rows:
                data = {
                    "id": int(row["id"]),
                    "event_id": int(row["event_id"]),
                    "type_entity": row.get("type_entity"),
                    "offset": int(row["offset"]) if row.get("offset") else None,
                    "length": int(row["length"]) if row.get("length") else None,
                    "url": row.get("url"),
                    "user": row.get("user"),
                    "language": row.get("language"),
                    "custom_emoji_id": row.get("custom_emoji_id"),
                }
                stmt = sa.insert(cls).values(**data)
                await conn.execute(stmt)
            await conn.commit()
