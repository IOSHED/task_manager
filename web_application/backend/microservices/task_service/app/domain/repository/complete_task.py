from app.infra.postgres.models.complete_task import CompleteTask
from usecase.repository import SQLAlchemyRepository


class CompleteTaskRepository(SQLAlchemyRepository):
    model = CompleteTask
