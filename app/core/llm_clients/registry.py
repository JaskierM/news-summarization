from typing import Callable

from app.core.registry.registry import Registry
from app.core.llm_clients.base import BaseLLMClient

LLM_CLIENT_REGISTRY = Registry[Callable[[], BaseLLMClient]]()


def get_llm_client(name: str) -> BaseLLMClient:
    return LLM_CLIENT_REGISTRY.get(name)()
