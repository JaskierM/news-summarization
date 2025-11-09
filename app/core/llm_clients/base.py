from typing import Sequence, Optional
from langchain_core.language_models.chat_models import BaseChatModel


class BaseLLMClient:

    def __init__(self, llm: Optional[BaseChatModel] = None):
        self._llm = llm

    @property
    def llm(self) -> BaseChatModel:
        return self._llm

    def chat(self, messages: Sequence[str], **kwargs) -> str:
        response = self._llm.invoke(list(messages), **kwargs)
        return response.content

    async def achat(self, messages: Sequence[str], **kwargs) -> str:
        response = await self._llm.ainvoke(list(messages), **kwargs)
        return response.content
