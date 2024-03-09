from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.domain.shemas.models.task import TaskSchema
from app.infra.postgres import db
from app.usecase.interfaces.to_read_model import IToReadModel
from app.domain.annotated_types.model import IntPk, DatetimeTimeZone, str_sized


class Task(db.Base, IToReadModel):
    """
    Модель, описывающая таблицу `Task`. Сдесь должна хранитьс основная информация о `Task`.\n

    :param id (int)                    - уникальный индификатор `Task`;\n
    :param id_template (Optional[int]) - id шаблона, от которого будут наследоваться значения полей `Task`;\n
    :param name (str)                  - имя `Task`;\n
    :param description (Optional[str]) - описание `Task`;\n
    :param create_by (int)             - id пользователя, создавшего эту `Task`;\n
    :param created_at (datetime)       - когда была создана задача;\n
    """
    __tablename__ = "task"

    id: Mapped[IntPk]
    create_by: Mapped[int]
    name: Mapped[str_sized(255)]

    id_template: Mapped[Optional[int]] = mapped_column(default=None)
    description: Mapped[Optional[str_sized(512)]] = mapped_column(default=None)
    created_at: Mapped[DatetimeTimeZone] = mapped_column(default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r})"

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            id_template=self.id_template,
            name=self.name,
            description=self.description,
            create_by=self.create_by,
            created_at=self.created_at,
        )
