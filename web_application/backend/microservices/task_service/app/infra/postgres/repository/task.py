from app.infra.postgres.models.task import Task
from app.infra.postgres.orm_repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
