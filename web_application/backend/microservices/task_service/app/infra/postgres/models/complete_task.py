from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.domain.shemas.models.complete_task import CompleteTaskSchema
from app.infra.postgres import db
from app.usecase.interfaces.to_read_model import IToReadModel
from usecase.annotated_types.model import IntPk, DatetimeTimeZone, foreign_key_delete_cascade


class CompleteTask(db.Base, IToReadModel):
    """
    Модель содержит записи о тех `Task`, которые должны будут завершины когда-то.\n

    :param id (int)                                 - уникальный индификатор `NotificationTask`;\n
    :param task_id (int)                            - id `Task`, к которому привязана эта запись;\n
    :param complete_at (Optional[datatime])         - когда была выполнена задача;\n
    :param planned_complete_at (Optional[datatime]) - время когда планируется завершить `Task`;\n
    """
    __tablename__ = "complete_task"

    id: Mapped[IntPk]
    task_id: Mapped[foreign_key_delete_cascade("task.id")] = mapped_column(unique=True)
    complete_at: Mapped[Optional[DatetimeTimeZone]] = mapped_column(default=None)
    planned_complete_at: Mapped[Optional[DatetimeTimeZone]] = mapped_column(default=None)

    def __repr__(self) -> str:
        return f"CompleteTask(id={self.id!r}, planned_complete_at={self.planned_complete_at!r})"

    def to_read_model(self) -> CompleteTaskSchema:
        return CompleteTaskSchema(
            id=self.id,
            task_id=self.task_id,
            complete_at=self.complete_at,
            planned_complete_at=self.planned_complete_at
        )
