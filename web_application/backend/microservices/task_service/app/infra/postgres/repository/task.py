from app.infra.postgres.models.task import Task
from app.infra.postgres.orm_repository import SQLAlchemyRepository
from app.domain.schemas.models.task import TaskSchema


class TaskRepository(SQLAlchemyRepository):
    model = Task
    view_schema = TaskSchema
