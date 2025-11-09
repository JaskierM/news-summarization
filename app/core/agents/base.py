from abc import ABC, abstractmethod
from typing import Sequence, Optional
from jinja2 import Environment, FileSystemLoader
from langchain.chat_models.base import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool

from app.core.llm_clients.registry import get_llm_client
from app.core.llm_clients.base import BaseLLMClient
from app.core.settings.agents import BaseAgentSettings
from app.core.settings.app import load_settings
from app.core.tools.registry import get_tool

_app_settings = load_settings()


class BaseAgent(ABC):

    def __init__(self, cfg: BaseAgentSettings):
        self._cfg = cfg

    @property
    def cfg(self) -> BaseAgentSettings:
        return self._cfg

    @abstractmethod
    def build(self) -> Runnable: ...

    def _load_llm_client(self) -> BaseLLMClient:
        llm_client = get_llm_client(self._cfg.llm_client_key)
        return llm_client

    def _load_llm(self) -> BaseChatModel:
        return self._load_llm_client().llm

    def _load_tools(self) -> Sequence[BaseTool]:
        return [get_tool(tool_key) for tool_key in self._cfg.tool_keys or []]

    def _load_prompt(self, globals: Optional[dict] = None) -> str:
        path = _app_settings.PROMPTS_PATH / f"{self._cfg.prompt_name}.jinja2"
        return (
            Environment(loader=FileSystemLoader(_app_settings.PROMPTS_PATH))
            .get_template(path.name, globals=globals)
            .render()
        )
