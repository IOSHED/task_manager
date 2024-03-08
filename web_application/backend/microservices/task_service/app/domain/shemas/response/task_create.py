from typing import Optional

import pydantic

from app.domain.shemas.models.task import TaskSchema
from app.domain.shemas.models.notification_task import NotificationTaskSchema
from app.domain.shemas.models.complete_task import CompleteTaskSchema


class ResponseTaskSchemaCreate(pydantic.BaseModel):
    task: TaskSchema
    notification: Optional[NotificationTaskSchema] = None
    complete: Optional[CompleteTaskSchema] = None
