from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.shemas.models.task import TaskSchema
from app.infra.postgres import db

from app.utils.interfaces.base import IToReadModel


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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_template: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, default=None)
    create_by: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

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
