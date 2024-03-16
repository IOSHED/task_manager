from datetime import datetime, time
from typing import Optional

import pydantic
from pydantic import PositiveInt, constr


class RequestTaskSchemaCreate(pydantic.BaseModel):
    id_template: Optional[PositiveInt] = None
    name: constr(min_length=1, max_length=255, pattern=r"[a-zA-Zа-яА-Я\'\"\_\!\.\,\(\)]")
    description: Optional[constr(max_length=255, pattern=r"[a-zA-Zа-яА-Я\'\"\_\!\.\,\(\)]")] = None

    send_notification_at: Optional[datetime] = None
    duration_send_notification_at: Optional[time] = None

    ability_to_complete_task: bool = False
    complete_at: Optional[datetime] = None
    planned_complete_at: Optional[datetime] = None
