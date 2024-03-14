import os
from pathlib import Path
from typing import List, Self, Optional, Type, Any

import pydantic
from pydantic import PositiveInt, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

from app.infra.config.yaml_loader import YamlLoadConfigWithInheritFiles
from app.infra.config.enums import Mode

_THIS_DIR = Path(__file__).parent
_MODE = Mode.get_by_str(mode) if (mode := os.getenv("MODE")) is not None else Mode.local


class Postgres(pydantic.BaseModel):
    user: str
    password: str
    db: str
    host: str
    port: PositiveInt

    database_url: Optional[PostgresDsn] = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)
        self.database_url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db}"


class Database(pydantic.BaseModel):
    postgres: Postgres


class BaseApp(pydantic.BaseModel):
    version_api: PositiveInt
    name_service: str
    origins: List[HttpUrl]

    path_service: Optional[str] = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)
        self.path_service = f"/api/v{self.version_api}/task"


class Request(pydantic.BaseModel):
    get_current_user: HttpUrl


class Settings(BaseSettings):
    """
    Корневой класс настроек проекта. Он загружает MODE из виртуального окружения и в зависимости от него подгружает
    либо local.yaml, либо dev.yaml. Всегда наследует значения из base.yaml. Реализует паттерн Singleton.

    Example:
    python
        settings = Settings()
        assert settings.mode == Mode.local
    """

    mode: Mode = _MODE
    base: BaseApp
    database: Database
    request: Request

    model_config = SettingsConfigDict(env_file='../../../.env', env_file_encoding='utf-8')
    __instance: Optional[Self] = None

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, PydanticBaseSettingsSource, YamlLoadConfigWithInheritFiles]:
        path_config = [
            Path(_THIS_DIR, "../../../config/dev.yaml" if _MODE == Mode.dev else "../../../config/local.yaml"),
            Path(_THIS_DIR, "../../../config/base.yaml"),
        ]
        return init_settings, env_settings, YamlLoadConfigWithInheritFiles(settings_cls, path_config)

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__instance is None:
            cls.__instance = super(Settings, cls).__new__(cls)
        return cls.__instance
