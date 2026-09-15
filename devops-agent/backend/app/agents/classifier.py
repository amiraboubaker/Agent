from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "security": ("secure", "security", "ssl", "tls", "secret", "credential", "firewall", "hardening"),
    "deployment": ("deploy", "release", "production", "vps", "server", "docker compose", "kubernetes", "k8s"),
    "troubleshooting": ("fail", "error", "broken", "debug", "incident", "outage", "logs", "troubleshoot"),
    "automation": ("automate", "ansible", "github actions", "ci/cd", "pipeline", "workflow", "script"),
    "monitoring": ("monitor", "metrics", "alert", "observability", "uptime", "prometheus", "grafana", "logging"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {
        task_type: sum(1 for keyword in keywords if keyword in normalized)
        for task_type, keywords in KEYWORDS.items()
    }
    return max(scores, key=scores.get) if max(scores.values()) else "general_infrastructure"
