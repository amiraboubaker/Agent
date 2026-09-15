import httpx

from app.core.config import Settings
from app.models.schemas import TaskType

SYSTEM_PROMPT = """You are an expert Mobile Application Development Agent.

MISSION:
Design, develop, debug, test, optimize, and deploy mobile applications.

EXPERTISE:
React Native, Expo, TypeScript, JavaScript, Flutter, Android, iOS, navigation, state management, REST APIs, authentication, maps, location, notifications, storage, performance optimization, and app deployment.

WORKFLOW:
1. Understand requirements.
2. Define application architecture.
3. Design navigation.
4. Define screens and components.
5. Implement features.
6. Integrate backend APIs.
7. Implement authentication and storage.
8. Test functionality.
9. Optimize performance.
10. Prepare release.

RULES:
- Follow platform best practices.
- Prefer reusable components.
- Keep UI responsive.
- Handle loading, errors, and empty states.
- Never invent APIs.
- Explain installation and build commands.

Always structure the response with these Markdown headings:
## Requirements
## Architecture
## Screens
## Components
## Implementation
## API Integration
## Testing
## Build
## Release

The user's classified task is: {task_type}."""


class LLMService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def answer(self, message: str, task_type: TaskType, history: list[dict[str, str]]) -> str:
        if not self.settings.llm_api_key and not self.settings.is_local_llm:
            return self._fallback_answer(message, task_type)
        payload = {"model": self.settings.llm_model, "messages": [{"role": "system", "content": SYSTEM_PROMPT.format(task_type=task_type)}, *history[-10:], {"role": "user", "content": message}], "temperature": 0.2}
        headers = {"Authorization": f"Bearer {self.settings.llm_api_key}"} if self.settings.llm_api_key else {}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.settings.llm_api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    @staticmethod
    def _fallback_answer(message: str, task_type: TaskType) -> str:
        return f"""## Requirements

Clarify the target platforms, users, primary flow, device constraints, and acceptance criteria for this **{task_type.replace('_', ' ')}** request.

## Architecture

Choose React Native with Expo or Flutter after confirming the team's existing skills and native-module needs. Keep domain logic, data access, and presentation independently testable.

## Screens

Map the happy path first, then define loading, error, empty, offline, permission, and authentication states for each screen.

## Components

Use small reusable components with typed props, platform-aware accessibility labels, and stable list keys.

## Implementation

Request: {message}

The local assistant is running without an LLM provider, so it has not generated project files or claimed an implementation was completed.

## API Integration

Document the real endpoint contract before coding. Add typed request and response models, timeout handling, retries only for safe operations, and secure token storage.

## Testing

Cover navigation, validation, loading and failure states, API parsing, and one end-to-end critical user journey.

## Build

For Expo, use `npx expo start` during development and `eas build` for release candidates. For native projects, verify debug builds on both target platforms.

## Release

Configure app identifiers, signing credentials, permissions, privacy disclosures, crash reporting, and store metadata. No release was performed in local fallback mode.
"""
