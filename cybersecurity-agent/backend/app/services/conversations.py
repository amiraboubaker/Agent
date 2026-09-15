import json
from datetime import UTC, datetime

from app.models.database import database
from app.models.schemas import ConversationSummary


def _now() -> str:
    return datetime.now(UTC).isoformat()


def create_conversation(title: str, task_type: str, messages: list[dict[str, str]]) -> int:
    cursor = database.execute(
        "INSERT INTO conversations (title, task_type, messages, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (title[:80], task_type, json.dumps(messages), _now(), _now()),
    )
    return int(cursor.lastrowid)


def get_conversation(conversation_id: int) -> dict | None:
    row = database.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,)).fetchone()
    if row is None:
        return None
    result = dict(row)
    result["messages"] = json.loads(result["messages"])
    return result


def update_conversation(conversation_id: int, messages: list[dict[str, str]]) -> None:
    database.execute(
        "UPDATE conversations SET messages = ?, updated_at = ? WHERE id = ?",
        (json.dumps(messages), _now(), conversation_id),
    )


def list_conversations() -> list[ConversationSummary]:
    rows = database.execute("SELECT * FROM conversations ORDER BY updated_at DESC").fetchall()
    return [
        ConversationSummary(
            id=row["id"],
            title=row["title"],
            task_type=row["task_type"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            message_count=len(json.loads(row["messages"])),
        )
        for row in rows
    ]
