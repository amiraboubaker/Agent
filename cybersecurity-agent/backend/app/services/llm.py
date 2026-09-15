import logging

import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert Cybersecurity Agent focused on authorized defensive security.

MISSION:
Identify security weaknesses and help users build secure systems.

EXPERTISE:
OWASP, secure coding, authentication, authorization, API security, network security, Linux security, Docker security, vulnerability analysis, threat modeling, encryption, secrets management, and security auditing.

WORKFLOW:
1. Understand the system.
2. Identify assets.
3. Identify attack surfaces.
4. Identify potential vulnerabilities.
5. Assess severity and risk.
6. Explain the vulnerability.
7. Provide defensive remediation.
8. Recommend security controls.
9. Provide validation steps.

RULES:
- Assume systems must be owned or explicitly authorized.
- Focus on defensive security.
- Never expose secrets or request passwords, API keys, or credentials.
- Warn before potentially destructive actions.
- Never claim a vulnerability exists without evidence.
- Prefer safe testing methods.

Always structure the response with these Markdown headings:
## System
## Threats
## Vulnerabilities
## Risk
## Recommended Fix
## Secure Implementation
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
        return f"""## System

    Analyze this authorized defensive-security request as a **{task_type.replace('_', ' ')}** task:

    > {message}

    ## Threats
    No system scope, assets, or threat actors were provided, so no threat has been established.

    ## Vulnerabilities
    No vulnerability is claimed without evidence. The local agent is running without an LLM provider and cannot inspect the system.

    ## Risk
    Risk cannot be assessed until the affected assets, exposure, likelihood, and impact are known.

    ## Recommended Fix
    Provide an authorized scope, architecture, relevant configuration, and safe test evidence. Remove secrets before sharing.

    ## Secure Implementation
    Use least privilege, strong authentication, input validation, secure defaults, encryption in transit and at rest, and managed secrets.

    ## Validation
    Validate with code review, dependency scanning, authenticated tests in a non-production environment, and monitoring.

    ## Prevention
    Configure `LLM_API_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env`, then restart the backend. Keep credentials out of prompts, logs, source control, and frontend code."""
