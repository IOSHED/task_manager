import logging
from typing import Any, Dict

from app.usecase.requests.send_notification.deleting import delete_send_notification
from app.usecase.requests.send_notification.send import send_notification
from app.usecase.uow.dependencies import UOWDep

from app.domain.schemas.requests.task_create import RequestTaskSchemaCreate
from app.domain.convector.data_for_notification_task import get_data_for_notification_task


logger = logging.getLogger("console_log")


class NotificationTaskService:
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def add_notification_task(
        self,
        task_create: RequestTaskSchemaCreate,
        task_id: int,
        message: Dict[str, Any],
    ) -> None:
        data_for_notification_task = get_data_for_notification_task(task_create, task_id)
        logger.debug(f"data for creating notification task -> {data_for_notification_task}")
        if data_for_notification_task is not None:
            await self.uow.notification_task.add_one(data=data_for_notification_task.model_dump())
            await send_notification(dict(data_for_notification_task), message)

    async def delete(self, notification_task_id) -> None:
        await self.uow.notification_task.delete_one(id=notification_task_id)
        await delete_send_notification(notification_task_id)
