from app.infra.postgres.models.task import Task
from app.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
