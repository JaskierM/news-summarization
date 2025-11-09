import os
import sys

from typing import Optional, ClassVar
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.utils.env_detect import Environment, detect_environment


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=True,
        env_file=None,
    )
    ENV: Environment = Field(Environment.dev, validation_alias="APP_ENV")

    PROJECT_NAME: str = "AI SberBPM"
    VERSION: str = "0.0.1"

    HOST: str = "0.0.0.0"
    PORT: int = 8080
    BASE_PREFIX: str = "/api/ai-sberbpm"
    DOCS: bool = True

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    _DEFAULT_WORKERS: ClassVar[int] = 1
    _DIR_LEVEL: ClassVar[int] = 3

    @property
    def PROD(self) -> bool:
        return self.ENV is Environment.prod

    @property
    def WORKERS(self) -> int:
        return self._DEFAULT_WORKERS if self.PROD else 1

    @property
    def RELOAD(self) -> bool:
        return not self.PROD

    @property
    def PROJECT_ROOT(self) -> Path:
        return Path(__file__).resolve().parents[self._DIR_LEVEL]

    @property
    def PROMPTS_PATH(self) -> Path:
        bundle_root = Path(getattr(sys, "_MEIPASS", self.PROJECT_ROOT))
        return bundle_root / "app" / "prompts"

    @property
    def CONFIGS_PATH(self) -> Path:
        bundle_root = Path(getattr(sys, "_MEIPASS", self.PROJECT_ROOT))
        return bundle_root / "app" / "configs"

    def get_gigachat_secret_path(self, secret_file_name: str) -> Optional[Path]:
        if self.PROD:
            return None
        return self.PROJECT_ROOT / "cert" / secret_file_name

    @property
    def KRB5_CONFIG_PATH(self) -> str:
        if self.PROD:
            return "/etc/krb5.conf"
        else:
            return str(self.PROJECT_ROOT / "deploy" / "krb5.conf")

    @property
    def KRB5_CACHE_PATH(self) -> str:
        return "/tmp/krb5"

    @property
    def KEYTAB_TMP_PATH(self) -> str:
        return "/tmp/keytab_file.keytab"

    @classmethod
    def load(cls) -> "AppSettings":
        env = detect_environment()
        os.environ.setdefault("APP_ENV", env.value)

        return cls()


@lru_cache
def load_settings() -> AppSettings:
    return AppSettings.load()
