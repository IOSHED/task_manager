from abc import ABC, abstractmethod
from typing import Optional, Any


class Cacher(ABC):
    expire: int = NotImplementedError

    @abstractmethod
    async def set(self, key: Any, value: Any, expire: Optional[int] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: Any) -> Any:
        raise NotImplementedError
