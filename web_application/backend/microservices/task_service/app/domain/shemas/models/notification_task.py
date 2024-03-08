from datetime import datetime, time
from typing import Optional

import pydantic
from pydantic import PositiveInt


class NotificationTaskSchema(pydantic.BaseModel):
    """Схема по модели `NotificationTask`"""

    id: PositiveInt
    task_id: PositiveInt
    send_notification_at: datetime
    duration_send_notification_at: Optional[time] = None

    class Config:
        from_attributes = True


class NotificationTaskSchemaCreate(pydantic.BaseModel):
    """Даные неоходимые для создания записи в базе данных"""

    task_id: PositiveInt
    send_notification_at: datetime
    duration_send_notification_at: Optional[time] = None
