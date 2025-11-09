from enum import Enum
from typing import Literal, Union, Annotated, Optional
from pydantic import BaseModel, Field


class UserContext(BaseModel):
    """Контекстная информация о странице откуда пользователь направил запрос."""

    block: Optional[str] = Field(None)
    org_unit: Optional[str] = Field(None)
    process_name: Optional[str] = Field(None)
    kp_id: Optional[str] = Field(None)


class AppChatRequest(BaseModel):
    session_id: str
    message: str
    context: Optional[UserContext]


class EventType(str, Enum):
    node_update = "node_update"
    error = "error"
    final = "final"


class GraphKind(str, Enum):
    main = "main"
    subgraph = "subgraph"


class StreamEventBase(BaseModel):
    type: EventType
    graph: Optional[GraphKind] = None
    node: Optional[str] = None
    content: list[str] = []


class NodeUpdateEvent(StreamEventBase):
    type: Literal["node_update"]
    final_answer: None = None


class ErrorEvent(StreamEventBase):
    type: Literal["error"]
    final_answer: None = None


class FinalEvent(StreamEventBase):
    type: Literal["final"]
    final_answer: str


StreamEvent = Annotated[
    Union[NodeUpdateEvent, ErrorEvent, FinalEvent],
    Field(discriminator="type"),
]
