import logging

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.infra.postgres.models.task import Task
from app.infra.postgres.orm_repository import SQLAlchemyRepository
from app.domain.schemas.models.task import TaskSchema, TaskSchemaGet, TaskSchemaRelationship

logger = logging.getLogger("console_log")


class TaskRepository(SQLAlchemyRepository):
    model = Task
    view_schema = TaskSchema

    async def find_task_by_id(self, id_task: int) -> TaskSchemaGet:
        stmt = (
            select(self.model)
            .filter_by(id=id_task)
            .options(
                selectinload(self.model.notification_task),
                selectinload(self.model.complete_task),
            )
        )
        logger.debug(f"generated stmt -> {stmt}")
        sql_res = await self.session.execute(stmt)
        res = TaskSchemaRelationship.model_validate(sql_res.scalar_one(), from_attributes=True)
        return TaskSchemaGet(
            task=res,
            notification=res.notification_task,
            complete=res.complete_task,
        )
