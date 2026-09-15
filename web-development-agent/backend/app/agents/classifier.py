import re

from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "requirements": ("requirement", "user story", "acceptance criteria", "scope", "specification"),
    "architecture": ("architecture", "system design", "component design", "monolith", "microservice"),
    "ui": ("ui", "ux", "wireframe", "design system", "responsive", "accessibility", "semantic html"),
    "frontend": ("react", "next.js", "typescript", "javascript", "css", "tailwind", "browser", "frontend"),
    "backend": ("backend", "node", "express", "fastapi", "api", "authentication", "authorization", "server"),
    "database": ("database", "sql", "postgres", "sqlite", "schema", "migration", "orm", "redis"),
    "testing": ("test", "testing", "vitest", "jest", "playwright", "e2e", "unit test"),
    "deployment": ("deploy", "deployment", "docker", "ci/cd", "hosting", "production", "nginx"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {
        task_type: sum(1 for keyword in keywords if re.search(rf"\b{re.escape(keyword)}\b", normalized))
        for task_type, keywords in KEYWORDS.items()
    }
    return max(scores, key=scores.get) if max(scores.values()) else "general_web"
