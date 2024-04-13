from enum import Enum
from typing import Self


class Mode(Enum):
    local = "local"
    dev = "dev"

    @staticmethod
    def get_by_str(string: str) -> Self:
        if string == "local":
            return Mode.local
        return Mode.dev
