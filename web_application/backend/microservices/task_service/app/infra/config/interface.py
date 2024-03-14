from abc import ABC, abstractmethod
from typing import Self


class Load(ABC):
    @abstractmethod
    def load(self) -> Self:
        raise NotImplementedError
