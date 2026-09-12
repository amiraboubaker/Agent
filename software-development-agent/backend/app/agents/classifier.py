from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "debugging": ("error", "bug", "broken", "exception", "traceback", "fails", "failure"),
    "architecture": ("architect", "architecture", "design", "system", "scalable", "microservice"),
    "testing": ("test", "testing", "pytest", "coverage", "assertion", "spec"),
    "refactoring": ("refactor", "cleanup", "maintainability", "duplicate", "simplify"),
    "documentation": ("document", "documentation", "readme", "explain", "guide", "api docs"),
    "coding": ("build", "create", "implement", "write", "code", "feature", "component"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {
        task_type: sum(1 for keyword in keywords if keyword in normalized)
        for task_type, keywords in KEYWORDS.items()
    }
    return max(scores, key=scores.get) if max(scores.values()) else "coding"
