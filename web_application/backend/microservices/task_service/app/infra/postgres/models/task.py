from datetime import datetime
from typing import Optional

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.postgres import db
from app.domain.annotated_types.model import IntPk, DatetimeTimeZone, str_sized


class Task(db.Base):
    """
    A model describing the `Task` table. Basic information about the `Task` should be stored here.\n

    :param id (int)                    - unique indicator `Task`;\n
    :param id_template (Optional[int]) - id template from which the values of the fields will be inherited`Task`;\n
    :param name (str)                  - name `Task`;\n
    :param description (Optional[str]) - description `Task`;\n
    :param create_by (int)             - id user creating this `Task`;\n
    :param created_at (datetime)       - when was the task created;\n
    """

    # config filed
    __tablename__ = "task"
    __table_args__ = (
        Index("idx_id_and_create_by", "id", "create_by"),
        Index("idx_search_name_description", "name", "description", postgresql_using="gin")
    )
    _repr_field = (
        "id",
        "name",
        "create_at",
    )
    complete_task: Mapped["CompleteTask"] = relationship(back_populates="task")
    notification_task: Mapped["NotificationTask"] = relationship(back_populates="task")

    # table filed
    id: Mapped[IntPk]
    create_by: Mapped[int]
    name: Mapped[str_sized(255)]
    id_template: Mapped[Optional[int]] = mapped_column(default=None)
    description: Mapped[Optional[str_sized(512)]] = mapped_column(default=None)
    created_at: Mapped[DatetimeTimeZone] = mapped_column(default=datetime.utcnow)
