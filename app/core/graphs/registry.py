from typing import Callable
from langchain_core.runnables import Runnable

from app.core.registry.registry import Registry
from app.core.settings.graphs import BaseGraphSettings

GRAPH_REGISTRY = Registry[Callable[[BaseGraphSettings | None], Runnable]]()


def get_graph(name: str) -> Runnable:
    return GRAPH_REGISTRY.get(name)()
