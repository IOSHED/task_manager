from pathlib import Path
from typing import List, Dict, Any

from pydantic.fields import FieldInfo
from pydantic.v1.utils import deep_update
from pydantic_settings import PydanticBaseSettingsSource, BaseSettings
from yaml import safe_load


class YamlLoadConfigWithInheritFiles(PydanticBaseSettingsSource):
    """
    Загружает .yaml или .yml файлы. Обновляет педыдущее значение или добавляет его к предыдущему загруженному файлу,
    реализовывая тем самым наследование config файлов.
    """

    def __init__(self, settings_cls: type[BaseSettings], path_configs: List[Path]) -> None:
        super().__init__(settings_cls)
        self.dict_config = {}
        self.config_file_settings(path_configs)

    def config_file_settings(self, path_configs: List[Path]) -> Dict[str, Any]:
        for path in path_configs:
            if not path.is_file():
                print(f"No file found at `{path.resolve()}`")
                continue
            if path.suffix in {".yaml", ".yml"}:
                self.dict_config = deep_update(self.dict_config, YamlLoadConfigWithInheritFiles.load_yaml(path))
            else:
                print(f"Unknown config file extension `{path.suffix}`")
        return self.dict_config

    @staticmethod
    def load_yaml(path: Path) -> Dict[str, Any]:
        with Path(path).open("r") as f:
            config = safe_load(f)
        if not isinstance(config, dict):
            raise TypeError(
                f"Config file has no top-level mapping: {path}"
            )
        return config

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        return self.dict_config[field_name], field_name, False

    def __call__(self) -> Dict[str, Any]:
        return self.dict_config
