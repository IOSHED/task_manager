from abc import ABC, abstractmethod
from typing import Type

from app.infra.postgres.db import async_session_maker
from app.domain.repository.task import TaskRepository
from app.domain.repository.complete_task import CompleteTaskRepository
from app.domain.repository.notification_task import NotificationTaskRepository


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


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        # Set tree repositories
        self.task = TaskRepository(self.session)
        self.complete_task = CompleteTaskRepository(self.session)
        self.notification_task = NotificationTaskRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
