import typing as t
import sqlalchemy as sa
from .base import METADATA


class SIRow(t.Protocol):
    id: int
    phone: str
    text: str


SITable: sa.Table = sa.Table(
    "site_info",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('phone', sa.String(255)),
    sa.Column('text', sa.Text()),
)
