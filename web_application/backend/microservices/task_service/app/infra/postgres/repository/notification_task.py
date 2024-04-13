from app.infra.postgres.models.notification_task import NotificationTask
from app.infra.postgres.orm_repository import SQLAlchemyRepository
from app.domain.schemas.models.notification_task import NotificationTaskSchema


class NotificationTaskRepository(SQLAlchemyRepository):
    model = NotificationTask
    view_schema = NotificationTaskSchema
