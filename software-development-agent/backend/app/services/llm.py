import logging

import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a senior software development agent. Give practical, production-quality answers. Structure responses with a short summary, assumptions, implementation guidance, validation steps, and risks when relevant. Use Markdown fenced code blocks with language tags. Never suggest executing untrusted generated code automatically. The user's classified task is: {task_type}."""


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
        return f"""## {task_type.title()} request received

I classified this request as **{task_type}**. Configure `LLM_API_KEY` in `.env` to enable generated guidance from your LLM provider.

### Request

> {message}

### Local agent behavior

The API is running safely in offline mode. It stores this conversation, preserves the task classification, and never executes generated code automatically.

### Next step

Set `LLM_API_URL`, `LLM_API_KEY`, and `LLM_MODEL`, then restart the backend to receive full implementation answers."""
