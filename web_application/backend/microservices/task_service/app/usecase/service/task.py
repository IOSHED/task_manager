from typing import Optional

from app.domain.shemas.requests.task_create import RequestTaskSchemaCreate
from app.usecase.convector.data_for_complete_task import get_data_for_complete_task
from app.usecase.convector.data_for_notification_task import get_data_for_notification_task
from app.usecase.convector.data_for_task import get_data_for_task
from app.utils.dependencies import UOWDep
from app.domain.shemas.response.task_create import ResponseTaskSchemaCreate
from app.domain.shemas.models.complete_task import CompleteTaskSchema
from app.domain.shemas.models.notification_task import NotificationTaskSchema


class TaskService:
    def __init__(self, uow: UOWDep):
        self.uow = uow

    async def create(self, task_create: RequestTaskSchemaCreate, user_id: int) -> ResponseTaskSchemaCreate:
        async with self.uow:
            task_id = await self.__add_task(task_create, user_id)
            notification_task = await self.__add_notification_task(task_create, task_id)
            complete_task = await self.__add_complete_task(task_create, task_id)

            new_task = await self.uow.task.find_one(id=task_id)

            await self.uow.commit()
            return ResponseTaskSchemaCreate(
                task=new_task,
                complete=complete_task,
                notification=notification_task,
            )

    async def __add_task(self, task_create: RequestTaskSchemaCreate, user_id: int) -> int:
        data_for_task = get_data_for_task(task_create, user_id)
        return await self.uow.task.add_one(data=data_for_task.model_dump())

    async def __add_notification_task(
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

    async def __add_complete_task(
        self,
        task_create: RequestTaskSchemaCreate,
        task_id: int,
    ) -> Optional[CompleteTaskSchema]:

        data_for_complete_task = get_data_for_complete_task(task_create, task_id)
        if data_for_complete_task is not None:
            complete_task_id = await self.uow.complete_task.add_one(data=data_for_complete_task.model_dump())
            return await self.uow.complete_task.find_one(id=complete_task_id)
        return None
