from datetime import UTC, datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from app.agents.classifier import classify_task
from app.core.config import Settings, get_settings
from app.models.schemas import ChatRequest, ChatResponse, ConversationSummary
from app.services.conversations import (
    create_conversation,
    get_conversation,
    list_conversations,
    update_conversation,
)
from app.services.llm import LLMService
from app.core.rate_limit import rate_limiter

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "product-management-agent"}


@router.get("/conversations", response_model=list[ConversationSummary])
def conversations() -> list[ConversationSummary]:
    return list_conversations()


@router.post("/chat", response_model=ChatResponse)
async def chat(http_request: Request, request: ChatRequest, settings: Settings = Depends(get_settings)) -> ChatResponse:
    client_ip = http_request.client.host if http_request.client else "unknown"
    if not rate_limiter.allow(client_ip, settings.rate_limit_per_minute):
        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
    task_type = classify_task(request.message)
    history: list[dict[str, str]] = []
    conversation_id = request.conversation_id
    if conversation_id is not None:
        conversation = get_conversation(conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        history = conversation["messages"]

    try:
        answer = await LLMService(settings).answer(request.message, task_type, history)
    except Exception:
        logger.exception("LLM provider request failed")
        raise HTTPException(status_code=502, detail="The AI provider is temporarily unavailable.") from None

    messages = [*history, {"role": "user", "content": request.message}, {"role": "assistant", "content": answer}]
    if conversation_id is None:
        conversation_id = create_conversation(request.message, task_type, messages)
    else:
        update_conversation(conversation_id, messages)

    return ChatResponse(
        conversation_id=conversation_id,
        task_type=task_type,
        answer=answer,
        created_at=datetime.now(UTC),
    )
