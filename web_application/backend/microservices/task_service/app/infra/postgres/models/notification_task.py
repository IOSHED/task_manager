from datetime import time
from typing import Optional

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.postgres import db
from app.domain.annotated_types.model import IntPk, DatetimeTimeZone, foreign_key_delete_cascade


class NotificationTask(db.Base):
    """
    The model contains records of those `Tasks` for which notifications need to be sent.\n

    :param id (int)                                       - unique indicator `NotificationTask`;\n
    :param task_id (int)                                  - id `Task` to which this record is linked;\n
    :param send_notification_at (datetime)                - date and time will send about `Task`;\n
    :param duration_send_notification_at (Optional[time]) - time for which you need to re-send a notification about `Task`;\n
    """

    # config field
    __tablename__ = "notification_task"
    __table_args__ = (
        Index("idx_id", "id"),
        Index("idx_send_notification_at", "send_notification_at"),
    )
    _repr_field = (
        "id",
        "task_id",
        "send_notification_at",
    )
    task: Mapped["Task"] = relationship(back_populates="notification_task")

    # table filed
    id: Mapped[IntPk]
    send_notification_at: Mapped[DatetimeTimeZone]
    task_id: Mapped[foreign_key_delete_cascade("task.id")] = mapped_column(unique=True)
    duration_send_notification_at: Mapped[Optional[time]] = mapped_column(default=None)
