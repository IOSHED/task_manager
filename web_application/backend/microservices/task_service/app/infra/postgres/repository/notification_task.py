from app.infra.postgres.models.notification_task import NotificationTask
from app.infra.postgres.orm_repository import SQLAlchemyRepository


class NotificationTaskRepository(SQLAlchemyRepository):
    model = NotificationTask
