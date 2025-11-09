from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Body

from app.core.states.api import AppChatRequest
from app.core.states.api import NodeUpdateEvent, ErrorEvent, FinalEvent
from app.core.streaming.flatten import flatten_event
from app.core.streaming.adapter import StreamAdapter
from app.services.graph_stream import event_source


event_schema = {
    "oneOf": [
        NodeUpdateEvent.model_json_schema(),
        ErrorEvent.model_json_schema(),
        FinalEvent.model_json_schema(),
    ],
    "description": (
        "NDJSON stream - каждая строка это один объект события. "
        "Поля: type ∈ {node_update,error,final}, graph ∈ {null,main,subgraph}, "
        "node ∈ {null,string}, content: string[], final_answer только при type='final'."
    ),
}
chat_router = APIRouter(prefix="/chat")


@chat_router.post(
    "/stream",
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "NDJSON stream (one JSON object per line)",
            "content": {
                "application/x-ndjson": {
                    "schema": event_schema,
                    "examples": {
                        "stream": {
                            "summary": "Пример потока",
                            "value": (
                                '{"type":"node_update","graph":"main","node":"plan","content":["sql_generated"]}\n'
                                '{"type":"node_update","graph":"subgraph","node":"tables_selector","content":["db_schema"]}\n'
                                '{"type":"final","graph":null,"node":null,"content":[],"final_answer":"32 клиента."}\n'
                            ),
                        }
                    },
                }
            },
        }
    },
)
async def stream_chat(payload: AppChatRequest | None = Body(None)) -> StreamingResponse:
    adapter = StreamAdapter()

    async def event_generator():
        try:
            async for raw in event_source(payload):
                for ev in flatten_event(raw, depth=0):
                    yield adapter.encode(ev)
        finally:
            for chunk in adapter.finalize_chunks():
                yield chunk

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
