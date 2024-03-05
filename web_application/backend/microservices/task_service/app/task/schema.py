import datetime
from typing import Optional

from pydantic import BaseModel, constr, PositiveInt, field_validator


class TaskBase(BaseModel):
    name: constr(min_length=1, max_length=255)
    description: constr(min_length=0, max_length=255)
    create_by: PositiveInt
    is_complete: Optional[bool]
    complete_at: Optional[datetime.datetime]
    planned_complete_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    send_notification_at: Optional[datetime.datetime]
    duration_repeat_send_notification_at: Optional[datetime.time]

    @classmethod
    @field_validator('complete_at', 'planned_complete_at', 'send_notification_at')
    def validate_completing(cls, v: datetime.datetime) -> datetime.datetime:
        if v < cls.created_at:
            raise ValueError('Datetime must be in the past')
        return v

    @classmethod
    @field_validator('created_at')
    def validate_creating(cls, v: datetime.datetime) -> datetime.datetime:
        if v > datetime.datetime.now():
            raise ValueError('Datetime must be in the future')
        return v


class TaskCreateSchema(TaskBase):
    template_id: PositiveInt


class TaskSchema(TaskBase):
    id: PositiveInt
    template_id: PositiveInt

    class Config:
        orm_mode = True
