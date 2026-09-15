from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "architecture": ("architecture", "expo", "react native", "flutter", "android", "ios", "structure"),
    "ui_ux": ("ui", "ux", "screen", "responsive", "component", "design", "accessibility"),
    "navigation": ("navigation", "route", "tab", "stack", "deep link", "screen flow"),
    "api_integration": ("api", "rest", "graphql", "authentication", "auth", "backend", "sync"),
    "testing": ("test", "debug", "detox", "unit", "e2e", "quality"),
    "performance": ("performance", "slow", "memory", "battery", "optimize", "offline"),
    "release": ("release", "deploy", "store", "build", "ios", "android", "submission"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {task_type: sum(keyword in normalized for keyword in keywords) for task_type, keywords in KEYWORDS.items()}
    best_score = max(scores.values())
    return max(scores, key=scores.get) if best_score else "general_mobile"
