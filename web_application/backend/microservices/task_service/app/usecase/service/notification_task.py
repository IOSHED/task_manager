from typing import Optional

from app.usecase.uow.dependencies import UOWDep

from app.domain.shemas.models.notification_task import NotificationTaskSchema
from app.domain.shemas.requests.task_create import RequestTaskSchemaCreate
from app.domain.convector.data_for_notification_task import get_data_for_notification_task


class NotificationTaskService:
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def add_notification_task(
        self,
        task_create: RequestTaskSchemaCreate,
        task_id: int,
    ) -> Optional[NotificationTaskSchema]:

        data_for_notification_task = get_data_for_notification_task(task_create, task_id)
        if data_for_notification_task is not None:
            notification_task_id = await self.uow.notification_task.add_one(
                data=data_for_notification_task.model_dump()
            )
            return await self.uow.notification_task.find_one(id=notification_task_id)
        return None
