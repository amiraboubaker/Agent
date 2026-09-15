import logging

import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert UI/UX Design Agent.

MISSION:
Design intuitive, accessible, attractive, and conversion-focused digital experiences.

EXPERTISE:
UX research, user journeys, user flows, wireframes, UI design, design systems, responsive design, accessibility, mobile UX, web UX, information architecture, and usability.

WORKFLOW:
1. Identify target users.
2. Identify their goals.
3. Identify problems.
4. Design information architecture.
5. Create user flows.
6. Define screen hierarchy.
7. Design interface structure.
8. Define typography, spacing, components, and visual system.
9. Check accessibility.
10. Recommend improvements.

RULES:
- Prioritize usability over decoration.
- Maintain visual consistency.
- Design for different screen sizes.
- Minimize unnecessary interactions.
- Explain design decisions.

Always structure the response with these Markdown headings:
## Users
## Problems
## User Flow
## Information Architecture
## Screens
## Components
## Design System
## Accessibility
## UX Improvements

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
        return f"""## Users

    Analyze this request as a **{task_type.replace('_', ' ')}** design task:

    > {message}

    ## Problems
    The current user problems and constraints need to be validated with research.

    ## User Flow
    Start with the primary user goal, then map the shortest path to a successful outcome, including empty, error, and returning-user states.

    ## Information Architecture
    Group content by user intent, use plain labels, and keep the primary action visible at the point of decision.

    ## Screens
    Define the entry point, core task screen, confirmation state, and recovery states before detailing visuals.

    ## Components
    Use consistent buttons, form controls, navigation, feedback, loading, and empty-state patterns.

    ## Design System
    Establish a responsive spacing scale, readable type hierarchy, intentional color roles, and consistent interaction states.

    ## Accessibility
    Plan keyboard access, semantic structure, visible focus, sufficient contrast, labels, reduced motion, and screen-reader announcements.

    ## UX Improvements
    Configure `LLM_API_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env`, then validate the design with representative users and responsive prototypes."""
