from datetime import datetime
from typing import Optional

import pydantic
from pydantic import PositiveInt, constr

from app.domain.schemas.models.complete_task import CompleteTaskSchema
from app.domain.schemas.models.notification_task import NotificationTaskSchema


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


class TaskSchemaRelationship(TaskSchema):
    notification_task: Optional[NotificationTaskSchema] = None
    complete_task: Optional[CompleteTaskSchema] = None


class TaskSchemaCreate(pydantic.BaseModel):
    """Даные неоходимые для создания записи в базе данных"""

    id_template: Optional[PositiveInt] = None
    name: constr(min_length=1, max_length=255, pattern=r"[a-zA-Zа-яА-Я\'\"\_\!\.\,\(\)]")
    description: Optional[constr(max_length=255, pattern=r"[a-zA-Zа-яА-Я\'\"\_\!\.\,\(\)]")] = None
    create_by: PositiveInt


class TaskSchemaGet(pydantic.BaseModel):
    task: TaskSchema
    notification_task: Optional[NotificationTaskSchema] = None
    complete_task: Optional[CompleteTaskSchema] = None
