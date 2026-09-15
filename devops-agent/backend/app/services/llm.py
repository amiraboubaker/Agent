import logging

import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert DevOps and Cloud Infrastructure Agent.

MISSION:
Deploy, automate, monitor, troubleshoot, and secure applications and infrastructure.

EXPERTISE:
Linux, Ubuntu, SSH, Ansible, Docker, Docker Compose, Kubernetes, Nginx, GitHub Actions, CI/CD, VPS, cloud infrastructure, networking, monitoring, logging, SSL/TLS, DNS, and server administration.

WORKFLOW:
1. Understand the infrastructure.
2. Identify the failing component.
3. Diagnose the problem.
4. Explain the root cause.
5. Provide exact commands.
6. Clearly identify where each command runs: [LOCAL WINDOWS], [WSL], [REMOTE VPS], or [CONTAINER].
7. Validate configuration.
8. Provide recovery steps.
9. Provide prevention steps.

RULES:
- Never assume a command succeeded.
- Never invent server state.
- Warn before destructive commands.
- Prefer reversible changes.
- Explain commands briefly.
- Never expose credentials.

Always structure the response with these Markdown headings:
## Problem
## Cause
## Solution
## Commands
## Validation
## Prevention

The user's classified task is: {task_type}."""


class LLMService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def answer(self, message: str, task_type: TaskType, history: list[dict[str, str]]) -> str:
        if not self.settings.llm_api_key and not self.settings.is_local_llm:
            return self._fallback_answer(message, task_type)
        self.settings.validate_llm_url()

        payload = {
            "model": self.settings.llm_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT.format(task_type=task_type)},
                *history[-10:],
                {"role": "user", "content": message},
            ],
            "temperature": 0.2,
        }
        headers = {}
        if self.settings.llm_api_key:
            headers["Authorization"] = f"Bearer {self.settings.llm_api_key}"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.settings.llm_api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        return data["choices"][0]["message"]["content"]

    @staticmethod
    def _fallback_answer(message: str, task_type: TaskType) -> str:
        return f"""## Problem

    Analyze this request as a **{task_type.replace('_', ' ')}** task:

    > {message}

    ## Cause
    No live infrastructure or command output was provided, so the failing component and root cause have not been verified.

    ## Solution
    The local agent is running without an LLM provider and cannot inspect or change infrastructure.

    ## Commands
    Provide the relevant command output first. Commands will be labeled `[LOCAL WINDOWS]`, `[WSL]`, `[REMOTE VPS]`, or `[CONTAINER]` and destructive actions will be called out.

    ## Validation
    No configuration or service state was validated.

    ## Prevention
    Configure `LLM_API_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env`, then restart the backend. Include the OS, deployment target, recent logs, and exact failing command in the next request."""
