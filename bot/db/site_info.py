import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, begin_connection


class SiteInfo(Base):
    __tablename__ = "site_info"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    text: Mapped[str] = mapped_column(sa.Text(), nullable=True)

    @classmethod
    async def old_data_insert(cls) -> None:
        """
        Reads old data from old_data/site_info.csv (with header)
        and bulk-inserts all rows into the site_info table.
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
                    "phone": row.get("phone"),
                    "text": row.get("text"),
                }
                stmt = sa.insert(cls).values(**data)
                await conn.execute(stmt)
            await conn.commit()
