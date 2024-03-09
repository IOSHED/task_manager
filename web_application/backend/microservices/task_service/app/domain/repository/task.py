from app.infra.postgres.models.task import Task
from usecase.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
