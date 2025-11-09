from typing import Optional
from pydantic import Field

from app.core.settings.base import BaseYamlSettings


class BaseGraphSettings(BaseYamlSettings):
    debug: Optional[bool] = Field(False)


class FullSummarizerGraphSettings(BaseGraphSettings):
    _config_name = "graphs"
    _config_section = "full_summarizer"
