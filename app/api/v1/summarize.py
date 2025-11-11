from fastapi import APIRouter, HTTPException, Body

from app.core.states.api import NewsSummarizationRequest, NewsSummarizationResponse
from app.services.graph_stream import event_source

summarize_router = APIRouter(prefix="/summarize")


@summarize_router.post("/news")
async def summarize(
    payload: NewsSummarizationRequest | None = Body(None),
) -> NewsSummarizationResponse:
    try:
        result = await event_source(payload)

        response = NewsSummarizationResponse(
            summarization=result["summarization"],
            ner_extraction=result["ner_extraction"],
        )
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
