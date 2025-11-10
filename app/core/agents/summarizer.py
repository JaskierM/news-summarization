import textwrap

from typing import Optional
from operator import itemgetter
from langchain_core.runnables import Runnable
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import PydanticOutputParser

from app.core.settings.agents import SummarizerAgentSettings
from app.core.agents.base import BaseAgent
from app.core.agents.registry import AGENT_REGISTRY
from app.core.states.agents.summarizer import NewsSummarization


class SummarizerAgent(BaseAgent):
    _user_prompt = HumanMessagePromptTemplate.from_template(
        textwrap.dedent(
            """
            Верни результат строго по схеме:
            {format_instructions}
            
            # Следующая новость:
            {input_news}
            """
        )
    )

    def __init__(self, cfg: Optional[SummarizerAgentSettings] = None):
        super().__init__(cfg)
        self._llm = self._load_llm()

        self._llm_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self._load_prompt()),
                self._user_prompt,
            ]
        )

    @property
    def cfg(self) -> SummarizerAgentSettings:
        return self._cfg

    def build(self) -> Runnable:
        parser = PydanticOutputParser(pydantic_object=NewsSummarization)
        prompt = self._llm_prompt.partial(
            format_instructions=parser.get_format_instructions()
        )

        return {"input_news": itemgetter("input_news")} | prompt | self._llm | parser


@AGENT_REGISTRY.register("summarizer")
def build() -> Runnable:
    return SummarizerAgent(SummarizerAgentSettings.from_yaml_config()).build()
