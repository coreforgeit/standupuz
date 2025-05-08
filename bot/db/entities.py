# import sqlalchemy as sa
# from sqlalchemy.orm import Mapped, mapped_column
# from .base import Base, begin_connection
#
#
# class Entity(Base):
#     __tablename__ = "entities"
#
#     id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
#     event_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
#     type_entity: Mapped[str] = mapped_column(sa.String(255), nullable=False)
#     offset: Mapped[int] = mapped_column(sa.Integer, nullable=True)
#     length: Mapped[int] = mapped_column(sa.Integer, nullable=True)
#     url: Mapped[str] = mapped_column(sa.String(255), nullable=True)
#     user: Mapped[str] = mapped_column(sa.String(255), nullable=True)
#     language: Mapped[str] = mapped_column(sa.String(255), nullable=True)
#     custom_emoji_id: Mapped[str] = mapped_column(sa.String(255), nullable=True)
#
#     @classmethod
#     async def add_entity(
#         cls,
#         event_id: int,
#         type_entity: str,
#         offset: int = None,
#         length: int = None,
#         url: str = None,
#         user: str = None,
#         language: str = None,
#         custom_emoji_id: str = None,
#     ) -> None:
#         stmt = sa.insert(cls).values(
#             event_id=event_id,
#             type_entity=type_entity,
#             offset=offset,
#             length=length,
#             url=url,
#             user=user,
#             language=language,
#             custom_emoji_id=custom_emoji_id,
#         )
#         async with begin_connection() as conn:
#             await conn.execute(stmt)
#             await conn.commit()
#
#     @classmethod
#     async def get_entities(cls, event_id: int) -> list[tuple]:
#         stmt = sa.select(cls).where(cls.event_id == event_id)
#         async with begin_connection() as conn:
#             result = await conn.execute(stmt)
#             return result.all()
#
#     @classmethod
#     async def delete_entities(cls, event_id: int) -> None:
#         stmt = sa.delete(cls).where(cls.event_id == event_id)
#         async with begin_connection() as conn:
#             await conn.execute(stmt)
#             await conn.commit()
#
#     @classmethod
#     async def old_data_insert(cls) -> None:
#         import csv
#         import json
#         from pathlib import Path
#         from typing import Dict, List, Optional
#         """
#         Читает CSV из db/old_data/entities.csv (с заголовком),
#         группирует данные в словарь {event_id: [dict, ...]},
#         делает JSON-дамп и сохраняет его в папку db/old_data/entities_json/entities_map.json
#         """
#         # Пути к файлам
#         data_dir = Path("db") / "old_data"
#         csv_path = data_dir / f"{cls.__tablename__}.csv"
#         map_path = data_dir / "id_map.json"
#         if not csv_path.exists() or not map_path.exists():
#             return
#
#         # Загрузка маппинга старых ID событий на новые
#         with map_path.open(encoding="utf-8") as mf:
#             raw_map = json.load(mf)
#         id_map: Dict[int, int] = {int(k): v for k, v in raw_map.items()}
#
#         # Чтение CSV и сборка словаря
#         entities_map: Dict[int, List[Dict]] = {}
#         with csv_path.open(newline="", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 print(row)
#                 old_event = int(row.get("event_id")) if row.get("event_id") else None
#                 new_event = id_map.get(old_event, old_event)
#
#                 entity_dict = {
#                     "type": row.get("type_entity"),
#                     "offset": int(row["offset"]) if row.get("offset") else None,
#                     "length": int(row["length"]) if row.get("length") else None,
#                     "url": row.get("url"),
#                     "user": row.get("user"),
#                     "language": row.get("language"),
#                     "custom_emoji_id": row.get("custom_emoji_id"),
#                 }
#                 entities_map.setdefault(new_event, []).append(entity_dict)
#
#         # Сохранение JSON-файла
#         # output_dir = data_dir / "entities_json"
#         # output_dir.mkdir(parents=True, exist_ok=True)
#         result_dict = {}
#         for k, v in entities_map.items():
#             result_dict[k] = json.dumps(v)
#
#         output_path = data_dir / "entities_map.json"
#         with output_path.open("w", encoding="utf-8") as jf:
#             json.dump(result_dict, jf, ensure_ascii=False, indent=2)
