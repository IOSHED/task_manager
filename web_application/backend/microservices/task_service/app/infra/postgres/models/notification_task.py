from datetime import time
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.domain.shemas.models.notification_task import NotificationTaskSchema
from app.infra.postgres import db
from app.infra.postgres.interface import IToReadModel
from app.domain.annotated_types.model import IntPk, DatetimeTimeZone, foreign_key_delete_cascade


class NotificationTask(db.Base, IToReadModel):
    """
    Модель содержит записи о тех `Task`, для которых нужно отправлять уведомляения.\n

    :param id (int)                                       - уникальный индификатор `NotificationTask`;\n
    :param task_id (int)                                  - id `Task`, к которому привязана эта запись;\n
    :param send_notification_at (datetime)                - дата и время, в которое будет отправлено уведомление о `Task`;\n
    :param duration_send_notification_at (Optional[time]) - премя за которое надо повторно отправить уведомление о `Task`;\n
    """
    __tablename__ = "notification_task"

    id: Mapped[IntPk]
    send_notification_at: Mapped[DatetimeTimeZone]

    task_id: Mapped[foreign_key_delete_cascade("task.id")] = mapped_column(unique=True)
    duration_send_notification_at: Mapped[Optional[time]] = mapped_column(default=None)

    def __repr__(self) -> str:
        return f"NotificationTask(id={self.id!r}, send_notification_at={self.send_notification_at!r})"

    def to_read_model(self) -> NotificationTaskSchema:
        return NotificationTaskSchema(
            id=self.id,
            task_id=self.task_id,
            send_notification_at=self.send_notification_at,
            duration_send_notification_at=self.duration_send_notification_at
        )
