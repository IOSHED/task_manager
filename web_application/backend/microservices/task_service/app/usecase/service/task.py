import logging
from typing import List

from app.domain.schemas.requests.task_create import RequestTaskSchemaCreate
from app.domain.schemas.response.task_create import ResponseTaskSchemaCreate
from app.domain.convector.data_for_task import get_data_for_task
from app.usecase.uow.dependencies import UOWDep
from app.usecase.service.notification_task import NotificationTaskService
from app.usecase.service.complete_task import CompleteTaskService
from app.domain.schemas.requests.task_delete import RequestTaskSchemaDelete
from app.usecase.requests.user.shemas import DataUser
from app.domain.schemas.response.task_get import ResponseTaskSchemaGet


logger = logging.getLogger("console_log")


class TaskService:
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def create(self, task_create: RequestTaskSchemaCreate, user_id: int) -> ResponseTaskSchemaCreate:
        async with self.uow:
            task_id = await self.__add_task(task_create, user_id)

            await NotificationTaskService(self.uow).add_notification_task(task_create, task_id)
            await CompleteTaskService(self.uow).add_complete_task(task_create, task_id)
            await self.uow.commit()

            new_task = await self.get_by_id(task_id)

            return ResponseTaskSchemaCreate(
                task=new_task.task,
                complete=new_task.complete,
                notification=new_task.notification,
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

            await self.uow.commit()

    async def get_by_id(self, id_task: int) -> ResponseTaskSchemaGet:
        async with self.uow:

            task_get_schema = await self.uow.task.find_task_by_id(id_task)

            return ResponseTaskSchemaGet(
                task=task_get_schema.task,
                complete=task_get_schema.complete_task,
                notification=task_get_schema.notification_task,
            )

    async def get_user_task(
        self,
        id_user: int,
        skip: int,
        limit: int,
        group_by: str,
    ) -> List[ResponseTaskSchemaGet]:
        async with self.uow:
            tasks_get_schema = await self.uow.task.find_user_task(id_user, skip, limit, group_by)

            return [
                ResponseTaskSchemaGet(
                    task=task_get_schema.task,
                    complete=task_get_schema.complete_task,
                    notification=task_get_schema.notification_task,
                ) for task_get_schema in tasks_get_schema
            ]


    async def __add_task(self, task_create: RequestTaskSchemaCreate, user_id: int) -> int:
        data_for_task = get_data_for_task(task_create, user_id)
        logger.debug(f"data for create task -> {data_for_task}")
        return await self.uow.task.add_one(data=data_for_task.model_dump())
