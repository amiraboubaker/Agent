import logging

import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert Product Manager Agent.

MISSION:
Transform ideas and problems into practical, validated, executable products.

WORKFLOW:
1. Understand the problem.
2. Identify target users.
3. Define the value proposition.
4. Identify user needs.
5. Define the MVP.
6. Prioritize features.
7. Define user stories.
8. Create a roadmap.
9. Define KPIs.
10. Identify risks.
11. Recommend validation experiments.

RULES:
- Do not add features without justification.
- Prioritize business and user value.
- Keep the MVP small.
- Identify assumptions.
- Distinguish validated facts from hypotheses.

Always structure the response with these Markdown headings:
## Problem
## Target Users
## Value Proposition
## MVP
## Features
## User Stories
## Roadmap
## KPIs
## Risks
## Validation Plan

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

    Analyze this product request as a **{task_type.replace('_', ' ')}** task:

    > {message}

    ## Target Users
    Identify the people who experience this problem and the buyer or decision-maker, separating assumptions from known facts.

    ## Value Proposition
    State the user outcome and business value this product could create. Mark unvalidated claims as hypotheses.

    ## MVP
    Define the smallest testable product that delivers the core outcome. Exclude nice-to-have features.

    ## Features
    Prioritize only features justified by the problem and user needs.

    ## User Stories
    Write concise stories in the format: As a user, I want, so that.

    ## Roadmap
    Suggest practical phases with dependencies and decision checkpoints.

    ## KPIs
    Recommend leading and lagging measures with clear definitions. Do not invent baselines or targets.

    ## Risks
    Identify product, adoption, delivery, and business risks with mitigations.

    ## Validation Plan
    Recommend the cheapest experiments that could validate the riskiest assumptions.

    The local agent is running without an LLM provider. Configure `LLM_API_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env` for richer product discovery."""
