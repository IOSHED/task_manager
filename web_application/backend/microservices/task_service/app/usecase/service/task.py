
from app.domain.shemas.requests.task_create import RequestTaskSchemaCreate
from app.domain.shemas.response.task_create import ResponseTaskSchemaCreate

from app.usecase.convector.data_for_task import get_data_for_task
from app.usecase.uow.dependencies import UOWDep
from app.usecase.service.notification_task import NotificationTaskService
from app.usecase.service.complete_task import CompleteTaskService


class TaskService:
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def create(self, task_create: RequestTaskSchemaCreate, user_id: int) -> ResponseTaskSchemaCreate:
        async with self.uow:
            task_id = await self.__add_task(task_create, user_id)
            notification_task = await NotificationTaskService(self.uow).add_notification_task(task_create, task_id)
            complete_task = await CompleteTaskService(self.uow).add_complete_task(task_create, task_id)

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
