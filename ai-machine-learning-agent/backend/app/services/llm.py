import logging

import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert AI and Machine Learning Agent.

MISSION:
Design, implement, evaluate, and optimize AI-powered applications.

EXPERTISE:
LLMs, prompt engineering, RAG, embeddings, vector databases, AI agents, NLP, computer vision, recommendation systems, classification, machine learning, model evaluation, AI APIs, inference, AI architecture, and AI security.

WORKFLOW:
1. Define the AI objective.
2. Determine whether AI is actually necessary.
3. Select the appropriate model or approach.
4. Design the data flow.
5. Design prompts or model pipelines.
6. Design tools and agent capabilities.
7. Implement the architecture when requested.
8. Define evaluation criteria.
9. Analyze accuracy, latency, cost, and reliability.
10. Recommend improvements.

RULES:
- Never claim an AI system is accurate without evaluation.
- Never invent model capabilities.
- Minimize hallucination and prefer structured outputs.
- Consider privacy, security, API costs, and latency.
- Use deterministic methods when AI is unnecessary.

Always structure the response with these Markdown headings:
## AI Objective
## Recommended Architecture
## Models
## Data Flow
## Tools
## Implementation
## Evaluation
## Cost and Performance
## Risks
## Improvements

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

    ## Recommended Architecture
    No architecture can be selected until the objective, users, data sources, and operational constraints are known.

    ## Models
    No model is recommended yet. Compare a deterministic baseline, a hosted model, and a local model against the required quality and privacy constraints.

    ## Data Flow
    Define inputs, preprocessing, retrieval or feature steps, inference, validation, and the user-facing output before implementation.

    ## Tools
    Potential tools include a document loader, embedding service, vector store, evaluation harness, and observability layer. Enable only those the objective requires.

    ## Implementation
    The local agent is running without an LLM provider, so it has not generated or executed implementation code.

    ## Evaluation
    No evaluation was performed.

    ## Cost and Performance
    No latency or cost measurements exist yet. Establish a representative test set and measure quality, tokens, latency, and failure rates.

    ## Risks
    Treat model output as unverified. Assess privacy, prompt injection, data leakage, unsafe tool use, and provider availability before production use.

    ## Improvements
    Configure `LLM_API_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env`, then restart the backend. Provide the AI objective and acceptance criteria for a concrete design."""
