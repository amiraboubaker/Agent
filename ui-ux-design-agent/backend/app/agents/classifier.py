from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "ux_research": ("user research", "interview", "persona", "usability", "user needs", "target users"),
    "user_flow": ("user flow", "journey", "workflow", "task flow", "navigation flow"),
    "information_architecture": ("information architecture", "sitemap", "content structure", "navigation", "taxonomy"),
    "ui_design": ("ui", "interface", "wireframe", "mockup", "component", "design system", "visual design"),
    "accessibility": ("accessibility", "wcag", "screen reader", "keyboard", "contrast", "inclusive"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {
        task_type: sum(1 for keyword in keywords if keyword in normalized)
        for task_type, keywords in KEYWORDS.items()
    }
    return max(scores, key=scores.get) if max(scores.values()) else "general_design"
