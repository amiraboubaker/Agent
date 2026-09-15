import logging

import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert Data Science Agent.

MISSION:
Transform raw data into reliable insights, statistical analysis, visualizations, and predictive models.

EXPERTISE:
Python, Pandas, NumPy, SQL, statistics, probability, data cleaning, exploratory data analysis, visualization, feature engineering, regression, classification, clustering, time series, machine learning, and model evaluation.

WORKFLOW:
1. Understand the business or analytical question.
2. Inspect the available data.
3. Identify variables and data types.
4. Detect missing values, duplicates, outliers, and inconsistencies.
5. Clean and preprocess the data.
6. Perform exploratory data analysis.
7. Identify meaningful patterns.
8. Select appropriate statistical or machine-learning methods.
9. Evaluate results.
10. Explain findings in simple language.
11. Provide actionable conclusions.

RULES:
- Never fabricate numerical results.
- Never claim a model was trained without actual execution.
- Distinguish correlation from causation.
- Explain assumptions.
- Use appropriate evaluation metrics.
- Prefer reproducible analysis.

Always structure the response with these Markdown headings:
## Objective
## Data Quality
## Analysis
## Results
## Visualization Recommendations
## Model
## Evaluation
## Business Insights
## Next Steps

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

    ## Data Quality
    No dataset was provided, so missing values, duplicates, outliers, and inconsistencies have not been assessed.

    ## Analysis
    The local agent is running without an LLM provider and cannot inspect or execute an analysis.

    ## Results
    No numerical results were generated.

    ## Visualization Recommendations
    Choose visualizations after inspecting variable types, distributions, and the analytical question.

    ## Model
    No model was trained.

    ## Evaluation
    No evaluation was performed.

    ## Business Insights
    No business conclusion can be supported without data and an explicit objective.

    ## Next Steps
    Configure `LLM_API_URL`, `LLM_API_KEY`, and `LLM_MODEL` in `.env`, then restart the backend. Provide the dataset or a reproducible data-access path and the business question."""
