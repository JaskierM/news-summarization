from typing import Callable
from langchain_core.runnables import Runnable

from app.core.registry.registry import Registry
from app.core.settings.agents import BaseAgentSettings

AGENT_REGISTRY = Registry[Callable[[BaseAgentSettings | None], Runnable]]()


def get_agent(name: str) -> Runnable:
    return AGENT_REGISTRY.get(name)()
