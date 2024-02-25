from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.v1 import validator


class TaskBase(BaseModel):
    name: str
    description: Optional[str]
    created_by: str
    created_at: datetime
    send_notification_at: datetime

    @validator('created_at', 'send_notification_at')
    def validate_datetime(self, v):
        if v < datetime.now():
            raise ValueError('Datetime must be in the future')
        return v


class TaskCreateSchema(TaskBase):
    pass


class TaskSchema(TaskBase):
    id: int
    template_id: int

    class Config:
        orm_mode = True
