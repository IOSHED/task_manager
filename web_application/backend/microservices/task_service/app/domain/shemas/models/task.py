from datetime import datetime
from typing import Optional

import pydantic
from pydantic import PositiveInt, constr


class TaskSchema(pydantic.BaseModel):
    """Схема по модели `Task`"""

    id: PositiveInt
    id_template: Optional[PositiveInt] = None
    name: constr(min_length=1, max_length=255, pattern=r"[a-zA-Zа-яА-Я\'\"\_\!\.\,\(\)]")
    description: Optional[constr(max_length=255, pattern=r"[a-zA-Zа-яА-Я\'\"\_\!\.\,\(\)]")] = None
    create_by: PositiveInt
    created_at: datetime = datetime.utcnow

    class Config:
        from_attributes = True


class TaskSchemaCreate(pydantic.BaseModel):
    """Даные неоходимые для создания записи в базе данных"""

    id_template: Optional[PositiveInt] = None
    name: constr(min_length=1, max_length=255, pattern=r"[a-zA-Zа-яА-Я\'\"\_\!\.\,\(\)]")
    description: Optional[constr(max_length=255, pattern=r"[a-zA-Zа-яА-Я\'\"\_\!\.\,\(\)]")] = None
    create_by: PositiveInt
