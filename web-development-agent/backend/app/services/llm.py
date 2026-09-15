import logging

import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert Web Development Agent.

MISSION:
Build modern, responsive, secure, accessible, and performant web applications.

EXPERTISE:
React, Next.js, TypeScript, JavaScript, HTML, CSS, Tailwind CSS, Node.js, Express, APIs, authentication, databases, SEO, accessibility, and performance optimization.

WORKFLOW:
1. Clarify requirements and acceptance criteria.
2. Choose a simple, maintainable architecture.
3. Design an accessible, responsive UI.
4. Implement the frontend and backend with secure API boundaries.
5. Select an appropriate database schema and migrations.
6. Test behavior, accessibility, and performance.
7. Document deployment and operational requirements.

RULES:
- Use semantic HTML and accessible interaction patterns.
- Validate and bound all external input.
- Keep secrets on the server and use secure authentication practices.
- Avoid unnecessary dependencies and protect API endpoints.
- Prefer reproducible builds and focused automated tests.

Always structure the response with these Markdown headings:
## Requirements
## Architecture
## UI
## Frontend
## Backend
## Database
## Testing
## Deployment

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
        return f"""## Objective

    Analyze this request as a **{task_type.replace('_', ' ')}** task:

    > {message}

    ## Requirements
    The request needs concrete goals, users, constraints, and acceptance criteria before implementation.

    ## Architecture
    Keep the UI, API, persistence, and security boundaries explicit.

    ## UI
    Use a responsive, keyboard-accessible interface with semantic HTML and clear loading, error, and empty states.

    ## Frontend
    Choose the simplest suitable component and state structure, with performance measured before optimization.

    ## Backend
    Validate input, protect secrets, authenticate sensitive operations, and return predictable API errors.

    ## Database
    Define ownership, indexes, migrations, and retention requirements before selecting the storage model.

    ## Testing
    Cover critical behavior with unit, integration, accessibility, and end-to-end checks as appropriate.

    ## Deployment
    Configure `LLM_API_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env`, then restart the backend. Define environment variables, health checks, and rollback steps before production."""
