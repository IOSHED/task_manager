from typing import Optional

from app.domain.shemas.models.notification_task import NotificationTaskSchemaCreate
from app.domain.shemas.requests.task_create import RequestTaskSchemaCreate


def get_data_for_notification_task(
    task_create: RequestTaskSchemaCreate,
    task_id: int
) -> Optional[NotificationTaskSchemaCreate]:
    if task_create.send_notification_at is None:
        return None
    return NotificationTaskSchemaCreate(
        task_id=task_id,
        send_notification_at=task_create.send_notification_at,
        duration_send_notification_at=task_create.duration_send_notification_at,
    )
