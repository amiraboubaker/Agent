from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "discovery": ("problem", "user", "customer", "interview", "need", "persona"),
    "strategy": ("value", "market", "position", "business", "opportunity", "vision"),
    "mvp": ("mvp", "minimum viable", "scope", "feature", "prioritize", "backlog"),
    "roadmap": ("roadmap", "milestone", "launch", "phase", "timeline", "release"),
    "validation": ("validate", "experiment", "test", "hypothesis", "kpi", "metric", "risk"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {
        task_type: sum(1 for keyword in keywords if keyword in normalized)
        for task_type, keywords in KEYWORDS.items()
    }
    return max(scores, key=scores.get) if max(scores.values()) else "general_product"
