from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    model = NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict):
        ...

    @abstractmethod
    async def find_all(self):
        ...

    @abstractmethod
    async def edit_one(self, data: dict, **filter_by) -> int:
        ...

    @abstractmethod
    async def find_one(self, **filter_by):
        ...

    @abstractmethod
    async def delete_all(self):
        ...

    @abstractmethod
    async def delete_one(self, **filter_by):
        ...
