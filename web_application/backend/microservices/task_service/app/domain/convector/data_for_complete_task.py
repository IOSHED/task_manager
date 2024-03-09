from typing import Optional

from app.domain.shemas.models.complete_task import CompleteTaskSchemaCreate
from app.domain.shemas.requests.task_create import RequestTaskSchemaCreate


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
