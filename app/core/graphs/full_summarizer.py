from typing import Any
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.core.states.graphs import FullSummarizerGraphState
from app.core.settings.graphs import FullSummarizerGraphSettings
from app.core.graphs.base import BaseGraph
from app.core.graphs.registry import GRAPH_REGISTRY
from app.core.agents.registry import get_agent


class FullSummarizerGraph(BaseGraph):

    def __init__(self, cfg: FullSummarizerGraphSettings):
        super().__init__(cfg)

        self._summarizer = get_agent("summarizer")
        self._ner_extractor = get_agent("ner_extractor")

    async def _summarizer_node(self, state: FullSummarizerGraphState) -> dict[str, Any]:
        summarization = await self._summarizer.ainvoke(
            {"input_news": state["input_news"]}
        )

        return {"summarization": summarization}

    async def _ner_extractor_node(
        self, state: FullSummarizerGraphState
    ) -> dict[str, Any]:
        ner_extraction = await self._ner_extractor.ainvoke(
            {"input_news": state["input_news"]}
        )
        return {"ner_extraction": ner_extraction}

    def build(self) -> Runnable:
        state_graph = StateGraph(FullSummarizerGraphState)

        state_graph.add_node("summarizer", self._summarizer_node)
        state_graph.add_node("ner_extractor", self._ner_extractor_node)

        state_graph.add_edge(START, "summarizer")
        state_graph.add_edge(START, "ner_extractor")
        state_graph.add_edge("summarizer", END)
        state_graph.add_edge("ner_extractor", END)

        return state_graph.compile(
            checkpointer=InMemorySaver(),
            debug=self._cfg.debug,
            name="full_summarizer",
        )


@GRAPH_REGISTRY.register("full_summarizer")
def build() -> Runnable:
    return FullSummarizerGraph(FullSummarizerGraphSettings.from_yaml_config()).build()
