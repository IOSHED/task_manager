from typing import Optional

import pydantic

from app.domain.schemas.models.task import TaskSchema
from app.domain.schemas.models.notification_task import NotificationTaskSchema
from app.domain.schemas.models.complete_task import CompleteTaskSchema


class ResponseTaskSchemaCreate(pydantic.BaseModel):
    task: TaskSchema
    notification: Optional[NotificationTaskSchema] = None
    complete: Optional[CompleteTaskSchema] = None
