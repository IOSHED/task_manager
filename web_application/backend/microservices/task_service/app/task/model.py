import datetime
from typing import Optional

from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.db.db import Base
from app.task.schema import TaskSchema


class Task(Base):
    __tablename__ = "task"

    """
    Модель, описывающая таблицу `Task`.
    
    :param id (int)          - уникальный индификатор `Task`;
    :param name (str)        - имя `Task`;
    :param description (str) - описание `Task`;
    :param create_by (int)   - id пользователя, создавшего эту `Task`;
    
    :param id_template (Optional[int])                                    - id шаблона, от которого будут 
                                                                            наследоваться значения полей `Task`;
    :param is_complete  (Optional[bool])                                  - завершена ли задача успешно;
    :param complete_at (Optional[datetime.datatime])                      - когда была выполнена задача;
    :param planned_complete_at (Optional[datetime.datatime])              - время когда планируется завершить `Task`;
    :param created_at (Optional[datetime.datetime])                       - когда была создана задача;
    :param send_notification_at (Optional[datetime.datetime])             - дата и время, в которое будет 
                                                                            отправлено уведомление о `Task`;
    :param duration_repeat_send_notification_at (Optional[datetime.time]) - премя за которое надо повторно 
                                                                            отправить уведомление о `Task`;
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    create_by: Mapped[int]

    id_template: Mapped[Optional[int]]
    is_complete: Mapped[Optional[bool]]
    complete_at: Mapped[Optional[datetime.datetime]]
    planned_complete_at: Mapped[Optional[datetime.datetime]]
    created_at: Mapped[Optional[datetime.datetime]]
    send_notification_at: Mapped[Optional[datetime.datetime]]
    duration_repeat_send_notification_at: Mapped[Optional[datetime.time]]

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r})"

    """Конвектирование значений таблицы в pydantic model"""
    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            name=self.name,
            description=self.description,
            create_by=self.create_by,
            id_template=self.id_template,
            is_complete=self.is_complete,
            complete_at=self.complete_at,
            planned_complete_at=self.planned_complete_at,
            created_at=self.created_at,
            send_notification_at=self.send_notification_at,
            duration_repeat_send_notification_at=self.duration_repeat_send_notification_at,
        )
