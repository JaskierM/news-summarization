from pydantic import Field

from app.core.settings.base import BaseYamlSettings


class BaseAgentSettings(BaseYamlSettings):
    llm_client_key: str = Field(...)
    prompt_name: str = Field(...)


class SummarizerAgentSettings(BaseAgentSettings):
    _config_name = "agents"
    _config_section = "summarizer"


class NERExtractorAgentSettings(BaseAgentSettings):
    _config_name = "agents"
    _config_section = "ner_extractor"
