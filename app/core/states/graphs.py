from typing import TypedDict

from app.core.states.agents.ner_extractor import NERExtraction


class FullSummarizerGraphState(TypedDict):
    session_id: str
    input_news: str
    summarization: str
    ner_extraction: NERExtraction
