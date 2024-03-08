
import pydantic


class IToReadModel:
    def to_read_model(self) -> pydantic.BaseModel:
        """Конвектирование значений таблицы в pydantic models"""
        raise NotImplementedError
