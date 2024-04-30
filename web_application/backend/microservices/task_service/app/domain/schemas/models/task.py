from datetime import datetime
from typing import Optional, Any

import pydantic
from pydantic import PositiveInt, constr

from app.domain.schemas.models.complete_task import CompleteTaskSchema
from app.domain.schemas.models.notification_task import NotificationTaskSchema


# TODO: rewrite docs
class TaskSchema(pydantic.BaseModel):
    """Схема по модели `Task`"""

    id: PositiveInt
    id_template: Optional[PositiveInt] = None
    name: constr(min_length=1, max_length=255, pattern=r"^[0-9a-zA-Zа-яА-ЯЁё\-\_\(\)\[\]\{\}\@\#\!\/\\\,\.\;]*$")
    description: Optional[constr(max_length=255, pattern=r"^[0-9a-zA-Zа-яА-ЯЁё\-\_\(\)\[\]\{\}\@\#\!\/\\\,\.\;]*$")] = None
    create_by: PositiveInt
    created_at: datetime = datetime.utcnow

    class Config:
        from_attributes = True


class TaskSchemaJoin(TaskSchema, CompleteTaskSchema, NotificationTaskSchema):
    task_id: PositiveInt
    complete_task_id: Optional[PositiveInt] = None
    notification_task_id: Optional[PositiveInt] = None

    # TODO: delete it
    # redefining a field inherited from other schemas for the `None` type in on sql query
    id: Optional[None] = None
    send_notification_at: Optional[datetime] = None


class TaskSchemaRelationship(TaskSchema):
    # TODO: replace type `Any`
    notification_task: Optional[Any]
    complete_task: Optional[Any]


class TaskSchemaCreate(pydantic.BaseModel):
    """Даные неоходимые для создания записи в базе данных"""

    id_template: Optional[PositiveInt] = None
    name: constr(min_length=1, max_length=255, pattern=r"^[0-9a-zA-Zа-яА-ЯЁё\-\_\(\)\[\]\{\}\@\#\!\/\\\,\.\;]*$")
    description: Optional[constr(max_length=255, pattern=r"^[0-9a-zA-Zа-яА-ЯЁё\-\_\(\)\[\]\{\}\@\#\!\/\\\,\.\;]*$")] = None
    create_by: PositiveInt


class TaskSchemaGet(pydantic.BaseModel):
    task: TaskSchema
    notification_task: Optional[NotificationTaskSchema] = None
    complete_task: Optional[CompleteTaskSchema] = None


class TaskSchemaFulltextSearch(pydantic.BaseModel):
    id: PositiveInt
    name: str
    description: str
