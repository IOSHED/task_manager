from typing import Optional

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.postgres import db
from app.domain.annotated_types.model import IntPk, DatetimeTimeZone, foreign_key_delete_cascade


class CompleteTask(db.Base):
    """
    The model contains records of those `Task` that will have to be completed sometime.\n

    :param id (int)                                 - unique indicator `NotificationTask`;\n
    :param task_id (int)                            - id `Task` which liked this record;\n
    :param complete_at (Optional[datatime])         - when the task was completed;\n
    :param planned_complete_at (Optional[datatime]) - tie when planned complete the `Task`;\n
    """

    # config filed
    __tablename__ = "complete_task"
    __table_args__ = (
        Index("idx_for_complete_task", "id"),
        Index("idx_planned_complete_at", "planned_complete_at"),
        Index("idx_complete_at", "complete_at"),
    )
    _repr_field = (
        "id",
        "task_id",
        "planned_complete_at",
    )
    task: Mapped["Task"] = relationship(back_populates="complete_task", cascade="all, delete")

    # table filed
    id: Mapped[IntPk]
    task_id: Mapped[foreign_key_delete_cascade("task.id")] = mapped_column(unique=True)
    complete_at: Mapped[Optional[DatetimeTimeZone]] = mapped_column(default=None)
    planned_complete_at: Mapped[Optional[DatetimeTimeZone]] = mapped_column(default=None)
