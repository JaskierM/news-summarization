from abc import ABC, abstractmethod
from langchain_core.runnables import Runnable

from app.core.settings.graphs import BaseGraphSettings


class BaseGraph(ABC):

    def __init__(self, cfg: BaseGraphSettings):
        self._cfg = cfg

    @property
    def cfg(self) -> BaseGraphSettings:
        return self._cfg

    @abstractmethod
    def build(self) -> Runnable: ...
