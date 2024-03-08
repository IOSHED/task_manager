from app.infra.postgres.models.notification_task import NotificationTask
from app.utils.repository import SQLAlchemyRepository


class NotificationTaskRepository(SQLAlchemyRepository):
    model = NotificationTask
