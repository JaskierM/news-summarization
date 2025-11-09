from typing import Callable
from langchain.tools import BaseTool

from app.core.registry.registry import Registry

TOOL_REGISTRY = Registry[Callable[[], BaseTool]]()


def get_tool(name: str) -> BaseTool:
    return TOOL_REGISTRY.get(name)()
