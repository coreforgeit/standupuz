import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy.dialects.postgresql as sa_postgresql
from datetime import datetime
import typing as t

from .base import Base, begin_connection
from settings.config import Config


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    username: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    last_visit: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    phone: Mapped[str] = mapped_column(sa.String(255), nullable=True)

    @classmethod
    async def add_user(
        cls,
        user_id: int,
        full_name: str,
        username: str,
        phone: str = None,
    ) -> None:
        now = datetime.now(Config.tz)
        stmt = (
            sa_postgresql.insert(cls)
            .values(
                user_id=user_id,
                full_name=full_name,
                username=username,
                last_visit=now,
                phone=phone,
            )
            .on_conflict_do_update(
                index_elements=[cls.user_id],
                set_={
                    "full_name": full_name,
                    "username": username,
                    "last_visit": now,
                },
            )
        )
        async with begin_connection() as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def get_user_info(cls, user_id: int) -> t.Optional[t.Self]:
        stmt = sa.select(cls).where(cls.user_id == user_id)
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_users(cls) -> list[t.Self]:
        stmt = sa.select(cls)
        async with begin_connection() as conn:
            result = await conn.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update_user_info(cls, user_id: int, phone: str = None) -> None:
        stmt = sa.update(cls).where(cls.user_id == user_id)
        if phone is not None:
            stmt = stmt.values(phone=phone)
        async with begin_connection() as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def old_data_insert(cls) -> None:
        """
        Reads old data from old_data/users.csv (with header)
        and bulk-inserts all rows into the users table.
        """
        import csv
        from pathlib import Path
        import sqlalchemy as sa
        from datetime import datetime

        file_path = Path("db/old_data") / f"{cls.__tablename__}.csv"
        if not file_path.exists():
            return

        with file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        async with begin_connection() as conn:
            for row in rows:
                data = {
                    # "id": int(row["id"]),
                    "user_id": int(row["user_id"]) if row.get("user_id") else None,
                    "full_name": row.get("full_name"),
                    "username": row.get("username"),
                    "last_visit": datetime.fromisoformat(row["last_visit"])
                                  if row.get("last_visit") else None,
                    "phone": row.get("phone"),
                }
                stmt = sa.insert(cls).values(**data)
                await conn.execute(stmt)
            await conn.commit()
