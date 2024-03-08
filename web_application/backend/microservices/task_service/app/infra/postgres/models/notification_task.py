from datetime import datetime, time
from typing import Optional

from sqlalchemy import Integer, DateTime, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.shemas.models.notification_task import NotificationTaskSchema
from app.infra.postgres import db
from app.utils.interfaces.base import IToReadModel


class NotificationTask(db.Base, IToReadModel):
    """
    Модель содержит записи о тех `Task`, для которых нужно отправлять уведомляения.\n

    :param id (int)                                       - уникальный индификатор `NotificationTask`;\n
    :param task_id (int)                                  - id `Task`, к которому привязана эта запись;\n
    :param send_notification_at (datetime)                - дата и время, в которое будет отправлено уведомление о `Task`;\n
    :param duration_send_notification_at (Optional[time]) - премя за которое надо повторно отправить уведомление о `Task`;\n
    """
    __tablename__ = "notification_task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    send_notification_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_send_notification_at: Mapped[Optional[time]] = mapped_column(Time, nullable=True, default=None)

    def __repr__(self) -> str:
        return f"NotificationTask(id={self.id!r}, send_notification_at={self.send_notification_at!r})"

    def to_read_model(self) -> NotificationTaskSchema:
        return NotificationTaskSchema(
            id=self.id,
            task_id=self.task_id,
            send_notification_at=self.send_notification_at,
            duration_send_notification_at=self.duration_send_notification_at
        )
