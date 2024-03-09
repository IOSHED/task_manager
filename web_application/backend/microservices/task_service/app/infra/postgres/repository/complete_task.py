from app.infra.postgres.models.complete_task import CompleteTask
from app.infra.postgres.orm_repository import SQLAlchemyRepository


class CompleteTaskRepository(SQLAlchemyRepository):
    model = CompleteTask
