
from typing import Dict, Any, List

import pydantic
from pydantic import PositiveInt, field_validator


# TODO: add validator for all field and for them types
class RequestUpdatingDataTaskSchema(pydantic.BaseModel):
    task_id: PositiveInt
    updating_field: Dict[str, Any]

    __field_task: List[str] = [
        "id_template",
        "name",
        "description",
        "create_by",
        "created_at",
    ]
    __field_notification_task: List[str] = [
        "send_notification_at",
        "duration_send_notification_at",
    ]
    __field_complete_task: List[str] = [
        "complete_at",
        "planned_complete_at",
    ]

    @classmethod
    @field_validator("updating_field")
    def __validate_updating_field(cls, v) -> Dict[str, Any]:
        allowed_keys = set(cls.field_task + cls.field_notification_task + cls.field_complete_task)
        input_keys = set(v.keys())
        if not input_keys.issubset(allowed_keys):
            raise pydantic.ValidationError
        return v

    async def get_field_task(self) -> Dict[str, Any]:
        return {key: value for key, value in self.updating_field.items() if key in self.__field_task}

    async def get_field_notification_task(self) -> Dict[str, Any]:
        return {key: value for key, value in self.updating_field.items() if key in self.__field_notification_task}

    async def get_field_complete_task(self) -> Dict[str, Any]:
        return {key: value for key, value in self.updating_field.items() if key in self.__field_complete_task}
