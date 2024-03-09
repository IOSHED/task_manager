from typing import Optional

from app.domain.shemas.models.complete_task import CompleteTaskSchema
from app.domain.shemas.requests.task_create import RequestTaskSchemaCreate
from app.usecase.uow.dependencies import UOWDep
from app.usecase.convector.data_for_complete_task import get_data_for_complete_task


class CompleteTaskService:
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def add_complete_task(
        self,
        task_create: RequestTaskSchemaCreate,
        task_id: int,
    ) -> Optional[CompleteTaskSchema]:

        data_for_complete_task = get_data_for_complete_task(task_create, task_id)
        if data_for_complete_task is not None:
            complete_task_id = await self.uow.complete_task.add_one(data=data_for_complete_task.model_dump())
            return await self.uow.complete_task.find_one(id=complete_task_id)
        return None
