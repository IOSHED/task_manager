from typing import Optional

from app.domain.schemas.models.complete_task import CompleteTaskSchemaCreate
from app.domain.schemas.requests.task_create import RequestTaskSchemaCreate


# TODO: delete this module and created this func in any class
# TODO: async function and create docs
def get_data_for_complete_task(
    task_create: RequestTaskSchemaCreate,
    task_id: int
) -> Optional[CompleteTaskSchemaCreate]:
    if task_create.ability_to_complete_task:
        return CompleteTaskSchemaCreate(
            task_id=task_id,
            complete_at=task_create.complete_at,
            planned_complete_at=task_create.planned_complete_at
        )
    return None
