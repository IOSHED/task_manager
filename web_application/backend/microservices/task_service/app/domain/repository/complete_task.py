from app.infra.postgres.models.complete_task import CompleteTask
from app.utils.repository import SQLAlchemyRepository


class CompleteTaskRepository(SQLAlchemyRepository):
    model = CompleteTask
