from typing import AsyncIterator

from app.core.registry.registry_loader import register_all
from app.core.states.api import AppChatRequest
from app.core.graphs.registry import get_graph


register_all()
data_copilot = get_graph("data_copilot")


async def event_source(payload: AppChatRequest | None = None) -> AsyncIterator:
    try:
        async for delta in data_copilot.astream(
            {
                "session_id": payload.session_id,
                "user_message": payload.message,
                "user_context": payload.context,
                "messages": {
                    "role": "user",
                    "content": f"Сообщение пользователя: {payload.message}",
                },
            },
            config={"configurable": {"thread_id": payload.session_id}},
            stream_mode=["updates", "custom"],
        ):
            yield delta

        last_message = (
            data_copilot.get_state(
                config={"configurable": {"thread_id": payload.session_id}}
            )
            .values["messages"][-1]
            .content
        )
        last_delta = ("final", {"output": {"last_message": last_message}})

        yield last_delta
    except Exception as e:
        error_delta = (
            "error",
            {"output": {"error": f"Error occurred during streaming: {e}"}},
        )
        yield error_delta
        return
