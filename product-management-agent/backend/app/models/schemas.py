from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

TaskType = Literal[
    "discovery",
    "strategy",
    "mvp",
    "roadmap",
    "validation",
    "general_product",
]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    conversation_id: int | None = Field(default=None, ge=1)


class ChatResponse(BaseModel):
    conversation_id: int
    task_type: TaskType
    answer: str
    created_at: datetime


class ConversationSummary(BaseModel):
    id: int
    title: str
    task_type: TaskType
    created_at: datetime
    updated_at: datetime
    message_count: int
