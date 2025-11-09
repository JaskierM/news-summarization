from typing import Optional
from langchain_community.chat_models import ChatOllama

from app.core.llm_clients.registry import LLM_CLIENT_REGISTRY
from app.core.llm_clients.base import BaseLLMClient
from app.core.settings.llm_clients import Qwen3Settings


class Qwen3LLMClient(BaseLLMClient):

    def __init__(self, cfg: Optional[Qwen3Settings] = None):
        llm = ChatOllama(
            model=cfg.model,
            base_url=cfg.base_url,
            format="json",
            temperature=cfg.temperature,
        )
        super().__init__(llm=llm)


@LLM_CLIENT_REGISTRY.register("qwen3")
def build() -> Qwen3LLMClient:
    return Qwen3LLMClient(Qwen3Settings.from_yaml_config())
