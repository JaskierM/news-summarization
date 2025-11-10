from pydantic import BaseModel

from app.core.states.agents.summarizer import NewsSummarization
from app.core.states.agents.ner_extractor import NERExtraction


class NewsSummarizationRequest(BaseModel):
    session_id: str
    input_news: str


class NewsSummarizationResponse(BaseModel):
    summarization: NewsSummarization
    ner_extraction: NERExtraction
