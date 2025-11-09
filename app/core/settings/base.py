import yaml

from typing import ClassVar, Type, TypeVar
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.settings.app import load_settings

_app_settings = load_settings()

T = TypeVar("T", bound="BaseYamlSettings")


class BaseYamlSettings(BaseSettings):
    _env_prefix: ClassVar[str] = ""
    _config_name: ClassVar[str] = ""
    _config_section: ClassVar[str] = ""

    model_config = ConfigDict(extra="ignore")

    @classmethod
    def from_yaml_config(cls: Type[T]) -> T:
        if not cls._config_name:
            raise ValueError("Config name must be specified in class")

        config_path = _app_settings.CONFIGS_PATH / f"{cls._config_name}.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f) or {}

        config_section = cls._config_section or cls.__name__.lower().replace(
            "settings", ""
        )
        if config_section and config_section in yaml_data:
            yaml_data = yaml_data[config_section]
        else:
            yaml_data = {}

        return cls(**yaml_data)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "_env_prefix") and cls._env_prefix:
            config_dict = dict(cls.model_config) if hasattr(cls, "model_config") else {}
            config_dict.update(
                {
                    "env_prefix": f"{cls._env_prefix}_",
                    "alias_generator": lambda field_name: f"{cls._env_prefix}_{field_name.upper()}",
                }
            )
            cls.model_config = SettingsConfigDict(**config_dict)
