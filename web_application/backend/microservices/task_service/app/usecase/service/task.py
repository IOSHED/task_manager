import logging

from app.domain.schemas.requests.task_create import RequestTaskSchemaCreate
from app.domain.schemas.response.task_create import ResponseTaskSchemaCreate

from app.domain.convector.data_for_task import get_data_for_task
from app.usecase.uow.dependencies import UOWDep
from app.usecase.service.notification_task import NotificationTaskService
from app.usecase.service.complete_task import CompleteTaskService
from app.domain.schemas.requests.task_delete import RequestTaskSchemaDelete
from app.usecase.requests.user.shemas import DataUser


logger = logging.getLogger("console_log")


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

    async def delete(self, args_query: RequestTaskSchemaDelete, user: DataUser) -> None:
        list_for_delete = args_query.id_for_deleting_tasks
        async with self.uow:
            if user.is_superuser:
                for id_task in list_for_delete:
                    await self.uow.task.delete_one(id=id_task)
                return

            for id_task in list_for_delete:
                await self.uow.task.delete_one(id=id_task, create_by=user.id)

    async def __add_task(self, task_create: RequestTaskSchemaCreate, user_id: int) -> int:
        data_for_task = get_data_for_task(task_create, user_id)
        logger.debug(f"data for create task -> {data_for_task}")
        return await self.uow.task.add_one(data=data_for_task.model_dump())
