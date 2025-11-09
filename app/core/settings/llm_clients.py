from typing import Optional
from pydantic import Field

from app.core.settings.base import BaseYamlSettings


class BaseLLMClientSettings(BaseYamlSettings):
    model: str = Field(...)
    base_url: Optional[str] = Field(None)
    temperature: Optional[float] = Field(0.2)
    max_tokens: Optional[int] = Field(None)


class Qwen3Settings(BaseLLMClientSettings):
    _config_name = "llm_clients"
    _config_section = "qwen3"
