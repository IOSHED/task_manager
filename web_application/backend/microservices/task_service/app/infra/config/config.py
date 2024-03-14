import os
from pathlib import Path
from typing import List, Self, Optional, Type

import pydantic
from pydantic import PositiveInt, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

from app.infra.config.interface import Load
from app.infra.config.yaml_loader import YamlLoadConfigWithInheritFiles
from app.infra.config.enums import Mode

_THIS_DIR = Path(__file__).parent
_MODE = Mode.get_by_str(mode) if (mode := os.getenv("MODE")) is not None else Mode.local


class Postgres(pydantic.BaseModel, Load):
    user: str
    password: str
    db: str
    host: str
    port: PositiveInt

    database_url: Optional[PostgresDsn] = None

    def load(self) -> Self:
        self.database_url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db}"
        return self


class Database(pydantic.BaseModel, Load):
    postgres: Postgres

    def load(self) -> Self:
        self.postgres.load()
        return self


class BaseApp(pydantic.BaseModel, Load):
    version_api: PositiveInt
    name_service: str
    origins: List[HttpUrl]

    path_service: Optional[str] = None

    def load(self) -> Self:
        self.path_service = f"/api/v{self.version_api}/task"
        return self


class Request(pydantic.BaseModel, Load):
    get_current_user: HttpUrl

    def load(self) -> Self:
        return self


class Settings(BaseSettings, Load):
    mode: Mode = _MODE
    base: BaseApp
    database: Database
    request: Request

    model_config = SettingsConfigDict(env_file='../../../.env', env_file_encoding='utf-8')

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

    def load(self) -> Self:
        """Дозагрузка данных на основе уже имеющихся"""
        self.base.load()
        self.database.load()
        self.request.load()

        return self


settings = Settings().load()
