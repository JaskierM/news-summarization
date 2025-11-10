from app.core.registry.registry_loader import register_all
from app.core.states.api import NewsSummarizationRequest, NewsSummarizationResponse
from app.core.graphs.registry import get_graph


register_all()
full_summarizer = get_graph("full_summarizer")


async def event_source(
    payload: NewsSummarizationRequest | None = None,
) -> NewsSummarizationResponse:
    response = await full_summarizer.ainvoke(
        {
            "session_id": payload.session_id,
            "input_news": payload.input_news,
        },
        config={"configurable": {"thread_id": payload.session_id}},
    )
    return response
