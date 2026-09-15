from datetime import UTC, datetime

from app.models.schemas import ConversationSummary, TaskType

_conversations: dict[int, dict] = {}
_next_id = 1


def create_conversation(message: str, task_type: TaskType, messages: list[dict[str, str]]) -> int:
    global _next_id
    now = datetime.now(UTC)
    conversation_id = _next_id
    _next_id += 1
    _conversations[conversation_id] = {"id": conversation_id, "title": message[:60], "task_type": task_type, "created_at": now, "updated_at": now, "messages": messages}
    return conversation_id


def get_conversation(conversation_id: int) -> dict | None:
    return _conversations.get(conversation_id)


def update_conversation(conversation_id: int, messages: list[dict[str, str]]) -> None:
    conversation = _conversations[conversation_id]
    conversation["messages"] = messages
    conversation["updated_at"] = datetime.now(UTC)


def list_conversations() -> list[ConversationSummary]:
    return [ConversationSummary(id=item["id"], title=item["title"], task_type=item["task_type"], created_at=item["created_at"], updated_at=item["updated_at"], message_count=len(item["messages"])) for item in sorted(_conversations.values(), key=lambda item: item["updated_at"], reverse=True)]
