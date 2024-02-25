from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, relationship

from app.db.db import Base


class Template(Base):
    __tablename__ = 'template'

    id = mapped_column(Integer, primary_key=True)
    tasks = relationship("Task", back_populates="template")

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, tasks={self.tasks!r})"
