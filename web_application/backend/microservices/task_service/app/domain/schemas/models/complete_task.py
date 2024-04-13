from datetime import datetime
from typing import Optional

import pydantic
from pydantic import PositiveInt


class CompleteTaskSchema(pydantic.BaseModel):
    """Схема по модели `CompleteTask`"""

    id: PositiveInt
    task_id: PositiveInt
    complete_at: Optional[datetime] = None
    planned_complete_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompleteTaskSchemaCreate(pydantic.BaseModel):
    """Даные неоходимые для создания записи в базе данных"""

    task_id: PositiveInt
    complete_at: Optional[datetime] = None
    planned_complete_at: Optional[datetime] = None
