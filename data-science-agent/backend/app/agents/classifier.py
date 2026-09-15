from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "data_quality": ("missing", "duplicate", "outlier", "inconsistent", "clean", "preprocess", "quality"),
    "eda": ("explore", "exploratory", "pattern", "distribution", "correlation", "insight"),
    "visualization": ("plot", "chart", "graph", "visualize", "visualization", "dashboard"),
    "statistics": ("statistic", "hypothesis", "probability", "significance", "test", "confidence"),
    "modeling": ("model", "regression", "classification", "clustering", "forecast", "predict", "machine learning", "feature"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {
        task_type: sum(1 for keyword in keywords if keyword in normalized)
        for task_type, keywords in KEYWORDS.items()
    }
    return max(scores, key=scores.get) if max(scores.values()) else "general_analysis"
