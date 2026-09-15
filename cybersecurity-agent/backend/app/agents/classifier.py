from app.models.schemas import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    "system_understanding": ("system", "asset", "architecture", "inventory", "scope", "environment"),
    "threat_modeling": ("threat", "attack surface", "threat model", "abuse case", "stride", "risk"),
    "vulnerability_analysis": ("vulnerability", "owasp", "injection", "xss", "csrf", "misconfiguration", "audit", "weakness"),
    "secure_implementation": ("secure", "authentication", "authorization", "encryption", "secrets", "docker", "hardening", "remediation"),
    "incident_response": ("incident", "breach", "compromise", "ransomware", "log", "containment", "forensics"),
}


def classify_task(message: str) -> TaskType:
    normalized = message.lower()
    scores = {
        task_type: sum(1 for keyword in keywords if keyword in normalized)
        for task_type, keywords in KEYWORDS.items()
    }
    return max(scores, key=scores.get) if max(scores.values()) else "general_security"
