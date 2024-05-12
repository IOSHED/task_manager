from abc import ABC, abstractmethod
from typing import Type

from app.infra.postgres.repository.complete_task import CompleteTaskRepository
from app.infra.postgres.repository.notification_task import NotificationTaskRepository
from app.infra.postgres.repository.task import TaskRepository


class IUnitOfWork(ABC):
    # Set tree repositories
    task: Type[TaskRepository]
    complete_task: Type[CompleteTaskRepository]
    notification_task: Type[NotificationTaskRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...
