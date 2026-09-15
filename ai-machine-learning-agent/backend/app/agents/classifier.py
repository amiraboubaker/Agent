from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "architecture": ("architecture", "pipeline", "system design", "inference", "agent"),
    "rag": ("rag", "retrieval", "embedding", "vector", "semantic search", "knowledge base"),
    "prompt_engineering": ("prompt", "structured output", "hallucination"),
    "evaluation": ("evaluate", "evaluation", "benchmark", "accuracy", "latency", "metric"),
    "security": ("security", "privacy", "prompt injection", "redact", "threat"),
    "implementation": ("implement", "build", "code", "api", "integrate", "recommendation", "classification"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {
        task_type: sum(1 for keyword in keywords if keyword in normalized)
        for task_type, keywords in KEYWORDS.items()
    }
    return max(scores, key=scores.get) if max(scores.values()) else "general_ai"
