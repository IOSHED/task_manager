from app.infra.postgres.models.notification_task import NotificationTask
from usecase.repository import SQLAlchemyRepository


class NotificationTaskRepository(SQLAlchemyRepository):
    model = NotificationTask
