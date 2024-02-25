
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column, relationship

from app.db.db import Base
from app.task.schema import TaskSchema


class Task(Base):
    __tablename__ = "task"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    description = mapped_column(String(255))

    template = relationship("Template", back_populates="tasks")

    created_at = mapped_column(DateTime(), server_default=func.CURRENT_TIMESTAMP())
    created_by = mapped_column()

    send_notification_at = mapped_column(DateTime())

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r})"

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            name=self.name,
            description=self.description,
            template=self.template,
            created_at=self.created_at,
            created_by=self.created_by,
            send_notification_at=self.send_notification_at,
        )
