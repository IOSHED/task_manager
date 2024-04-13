from app.infra.postgres.models.complete_task import CompleteTask
from app.infra.postgres.orm_repository import SQLAlchemyRepository
from app.domain.schemas.models.complete_task import CompleteTaskSchema


class CompleteTaskRepository(SQLAlchemyRepository):
    model = CompleteTask
    view_schema = CompleteTaskSchema
