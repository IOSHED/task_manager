import logging
from typing import Optional

from app.domain.schemas.models.complete_task import CompleteTaskSchema
from app.domain.schemas.requests.task_create import RequestTaskSchemaCreate
from app.usecase.uow.dependencies import UOWDep
from app.domain.convector.data_for_complete_task import get_data_for_complete_task


logger = logging.getLogger("console_log")


class CompleteTaskService:
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def add_complete_task(
        self,
        task_create: RequestTaskSchemaCreate,
        task_id: int,
    ) -> Optional[CompleteTaskSchema]:

        data_for_complete_task = get_data_for_complete_task(task_create, task_id)
        logger.debug(f"data for creating complete task -> {data_for_complete_task}")
        if data_for_complete_task is not None:
            complete_task_id = await self.uow.complete_task.add_one(data=data_for_complete_task.model_dump())
            return await self.uow.complete_task.find_one(id=complete_task_id)
        return None
