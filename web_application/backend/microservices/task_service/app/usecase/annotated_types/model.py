from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import mapped_column

IntPk = Annotated[int, mapped_column(primary_key=True)]

DatetimeTimeZone = Annotated[datetime, mapped_column(DateTime(timezone=True))]


def str_sized(max_length: int) -> type[str]:
    """Генерирует тип `mapped_column(String(max_length))`, где max_length вы указываете как аргумент."""
    return Annotated[str, mapped_column(String(max_length))]


def foreign_key_delete_cascade(column_key: str) -> type[int]:
    """Генерирует тип `mapped_column(ForeignKey(column_key, ondelete="CASCADE"))`, где column_key вы указываете как аргумент."""
    return Annotated[int, mapped_column(ForeignKey(column_key, ondelete="CASCADE"))]
