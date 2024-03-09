from app.domain.shemas.models.task import TaskSchemaCreate
from app.domain.shemas.requests.task_create import RequestTaskSchemaCreate


def get_data_for_task(task_create: RequestTaskSchemaCreate, user_id: int) -> TaskSchemaCreate:
    return TaskSchemaCreate(
        id_template=task_create.id_template,
        name=task_create.name,
        description=task_create.description,
        create_by=user_id,
    )
