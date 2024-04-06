import logging
from typing import List, Optional

from sqlalchemy import select, text, desc
from sqlalchemy.orm import selectinload, aliased

from app.infra.postgres.models.task import Task
from app.infra.postgres.orm_repository import SQLAlchemyRepository
from app.domain.schemas.models.task import TaskSchema, TaskSchemaGet, TaskSchemaRelationship, TaskSchemaJoin
from app.infra.postgres.repository.complete_task import CompleteTaskRepository
from app.infra.postgres.repository.notification_task import NotificationTaskRepository

# logger = logging.getLogger("console_log")


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
        sql_res = await self.session.execute(stmt)
        res = sql_res.scalar_one()
        res = TaskSchemaRelationship.model_validate(res, from_attributes=True)
        return TaskSchemaGet(
            task=self.view_schema.model_validate(
                res, from_attributes=True,
            ),
            notification_task=NotificationTaskRepository.view_schema.model_validate(
                res.notification_task, from_attributes=True,
            ) if res.notification_task is not None else None,
            complete_task=CompleteTaskRepository.view_schema.model_validate(
                res.complete_task, from_attributes=True,
            ) if res.complete_task is not None else None,
        )

    async def find_user_task(
            self,
            id_user: int,
            skip: int,
            limit: int,
            order_by: str,
            desc_res: bool = True,
            id_template: Optional[int] = None,
            is_show_notification: Optional[bool] = None,
            is_show_complete: Optional[bool] = None,
    ) -> List[TaskSchemaGet]:
        n = aliased(NotificationTaskRepository.model)
        c = aliased(CompleteTaskRepository.model)
        t = aliased(self.model)

        stmt = (
            select(
                t.id.label("task_id"), c.id.label("complete_task_id"), n.id.label("notification_task_id"),
                t.create_by, t.name, t.id_template, t.description, t.created_at,
                n.send_notification_at, n.duration_send_notification_at,
                c.complete_at, c.planned_complete_at,
            )
            .join(n, t.id == n.task_id, isouter=True)
            .join(c, t.id == c.task_id, isouter=True)
            # TODO: refactoring
            .filter(
                t.create_by == id_user,

                t.id_template == id_template if id_template else True,

                True is not None if is_show_notification is None
                else text("notification_task_1.id IS NOT NULL") if is_show_notification
                else text("notification_task_1.id IS NULL"),

                True if is_show_complete is None
                else text("complete_task_1.id IS NOT NULL") if is_show_complete
                else text("complete_task_1.id IS NULL"),
            )
            .order_by(desc(text(order_by)) if desc_res else text(order_by))
            .slice(skip, skip + limit)
        )
        sql_results = await self.session.execute(stmt)
        results = [
            TaskSchemaJoin.model_validate(sql_res, from_attributes=True)
            for sql_res in sql_results.all()
        ]

        # TODO: refactoring
        list_task_schemas = []
        for res in results:
            res.id = res.task_id
            task = self.view_schema(**res.model_dump())

            notification_task = None
            if res.notification_task_id is not None:
                res.id = res.notification_task_id
                notification_task = NotificationTaskRepository.view_schema(**res.model_dump())

            complete_task = None
            if res.complete_task_id is not None:
                res.id = res.complete_task_id
                complete_task = CompleteTaskRepository.view_schema(**res.model_dump())

            list_task_schemas.append(TaskSchemaGet(
                task=task,
                notification_task=notification_task,
                complete_task=complete_task,
            ))

        return list_task_schemas
